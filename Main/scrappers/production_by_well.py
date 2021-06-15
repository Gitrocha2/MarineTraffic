import io
import re
import datetime as dt

import csv
import requests
from bs4 import BeautifulSoup as bs

import db_helper as db
from wmscrape import runtime, helpers
from wmscrape.runtime.logger import get_logger

THIS_RUN_DATE = dt.datetime.now()
EXISTING_FILES = {}

HOME_PAGE_URL = 'http://www.anp.gov.br'
# PROD_PAGE_URL = 'http://dados.gov.br/dataset/dados-historicos-com-producao-de-petroleo-e-gas-natural-terra-e-mar'
url = 'http://www.anp.gov.br/conteudo-do-menu-superior/31-dados-abertos/5538-producao-de-petroleo-e-gas-natural-nacional'
FULL_MONTHS = {
    'janeiro': 1, 'fevereiro': 2, u'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
}
COL_HEADER_MAPPING = {
    'Ano': 'decYear',
    'Mês/Ano': 'dteProductionDate',
    'Estado': 'strStateName',
    'Bacia': 'strBasinName',
    'Campo': 'strFieldName',
    'Poço': 'strWellName',
    'Instalação': 'strInstallation',
    'Produção de Óleo (m³)': 'decOilProd',
    'Produção de Condensado (m³)': 'decCondProd',
    'Produção de Gás Associado (Mm³)': 'decAssociatedGasProd',
    'Produção de Gás Não Associado (Mm³)': 'decNonAssociatedGasProd',
    'Produção de Água (m³)': 'decWaterProd',
    'Injeção de Gás (Mm³)': 'decGasInjection',
    'Injeção de Água para Recuperação Secundária (m³)': 'decWaterInjectionRecovery',
    'Injeção de Água para Descarte (m³)': 'decWaterInjectionDisposal',
    'Injeção de Gás Carbônico (Mm³)': 'decCarbonicGasInjection',
    'Injeção de Nitrogênio (Mm³)': 'decNitrogenInjection',
    'Injeção de Vapor de Água (t)': 'decWaterVaporInjection',
    'Injeção de Polímeros (m³)': 'decPolymersInjection',
    'Injeção de Outros Fluidos (m³)': 'decOtherFluidsInjection'
}

logger = get_logger(__name__)
logger.info('starting')

'''
def get_last_run_date():

    return files name and their last updated date
    return: {
        'f_name_1': last updated date,
        'f_name_2': last updated date,
        ...
    }

    logger.info('getting last run dates')

    tbl = db.METADATA.tables['tblWellProdRaw']
    query = db.select([
        tbl.c.strFileName,
        db.func.max(tbl.c.dteRunDate).label('dteLastRunDate')
    ])
    query = query.group_by(tbl.c.strFileName)

    records = db.ENGINE.execute(query)

    results = {}

    for record in records:
        results[record['strFileName']] = record['dteLastRunDate']

    return results

'''


def save_to_csv(f_name, data):
    '''
    save a list of dicts to csv file
    '''

    logger.info('saving to db')

    with open('scrapers/brazil/downloads/' + f_name, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def save_to_db(data, csvname):
    '''
    insert list of dicts to database
    '''

    logger.info('deleting the records already present for the file')

    stmts = db.build_delete_stmts(data, 'tblWellProdRaw', csvname)
    result = db.execute_sql_stmts(stmts)

    logger.info('saving to db')

    stmts = db.build_insert_stmts(data, 'tblWellProdRaw')
    result = db.execute_sql_stmts(stmts)

    if result is True:
        logger.info('successfully inserted into db')
    else:
        logger.warning('unable to insert into db')


@runtime.processor
def get_files(body, scraper, context):
    '''
    get urls to info page and csv for each item
    '''

    logger.info('getting list of files from page')

    if context.get('cached') is False:
        scraper.do.persist(data=body, key=context.get('key'), type='html')

    # response = requests.get(body)

    # soup = bs(response.content, 'lxml')
    soup = bs(body, 'lxml')

    # find the list that contains string: Dados de produção de petróleo e gás natural

    # items=soup.find('h1', text = re.compile('Produção de petróleo e gás natural nacional'))

    # find parent element of the text
    # parentelement=items.find_parent('ul')

    # csv_a = parentelement.find_all('a', attrs={ 'href': re.compile('.csv$') })
    csv_a = soup.find_all('a', attrs={'href': re.compile('.csv$')})

    csv_final = []
    csv_final.append(csv_a[0])

    for i in range(len(csv_a)):
        if '1941-1979' in csv_a[i]:
            csv_final.append(csv_a[i + 1])
            break

    for item in csv_final:
        csv_url = item.attrs['href']
        csv_name = csv_url.split('/')[-1]
        info_url = HOME_PAGE_URL + csv_url

        this_context = context.copy()
        this_context['csv_name'] = csv_name
        this_context['csv_url'] = csv_url
        this_context['address'] = info_url

        scraper.do.http_get(
            url=this_context['address'],
            send_to=parse_csv,
            context=this_context,
            max_age=24
        )

        # response = requests.get(info_url)

        # parse_csv(response.content)


@runtime.processor
def parse_csv(body, scraper, context):
    '''
    extract data from csv file
    1. check if it's proper csv file
    2. choose proper encoding based on the starting string
    3. process string body for special case
    4. convert string to csv object
    5. process each line in the csv object
        a. each column might require different processing
    '''

    logger.info('parsing csv')

    if context.get('cached') is False:
        scraper.do.persist(data=body, key=context.get('key'), type='csv')

    # check if valid csv
    if b'<!DOCTYPE html>' in body:
        logger.warning('not valid csv')
        return

    # choose proper encoding
    if body[:3] == b'\xef\xbb\xbf':
        encoder = 'utf-8-sig'
    else:
        encoder = 'latin-1'

    logger.info('using {} encoding on file {}.'.format(
        encoder, context['csv_name']))

    a_very_long_str = body.decode(encoder)  # convert to string

    # to handle cases where line is wrapped in double quote
    # and numerical fields are wrapped in double double quote
    if a_very_long_str.find('""') > -1:
        a_very_long_str = a_very_long_str.replace('""', '||')  # replace "" with ||
        a_very_long_str = a_very_long_str.replace('"', '')  # replace " with nothing
        a_very_long_str = a_very_long_str.replace('||', '"')  # replace || with "

    # read string
    csv_reader = csv.DictReader(io.StringIO(a_very_long_str), delimiter=',')

    # read each line of csv file
    records = []
    # store column against file name which we need to delete first
    column = []

    for line in csv_reader:
        record = {
            'strFileName': context['csv_name'],
            'dteRunDate': THIS_RUN_DATE,
            'strEncoder': encoder
        }
        # depending on columns, perform different conversion
        for col, col_db in COL_HEADER_MAPPING.items():

            # if len of val is 0, set to None
            val = line[col] if len(line[col]) > 0 else None

            if val is None:
                record[col_db] = val
                continue

            # for numerical values, replace , with . then convert to float
            if 'Injeção' in col or 'Produção' in col:
                val = float(val.replace(',', '.'))

            # for month year, convert to date
            elif 'Mês/Ano' in col:
                val = dt.datetime.strptime('01/' + val, '%d/%m/%Y')

            record[col_db] = val  # assign new value

        records.append(record)
    column.append('strFileName')

    # save_to_csv(context['csv_name'], records)
    save_to_db(records, column)
    # print(records)

    return


# Main entry point
def main():
    scraper = runtime.create_aws_scraper()

    # Initial command
    scraper.do.http_get(
        url=url,
        send_to=get_files,
        max_age=24
    )

    scraper.start()


if __name__ == '__main__':
    scraper = runtime.create_local_scraper()

    # EXISTING_FILES = get_last_run_date()

    scraper.do.http_get(
        url=url,
        send_to=get_files,
        max_age=24
    )

    scraper.start()

    # get_files(url)
