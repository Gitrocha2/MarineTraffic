import requests
#import os
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from datetime import date
from dateutil.relativedelta import relativedelta
#from sqlalchemy import create_engine

#engine = create_engine('postgresql://' + os.environ.get('DB_USER') + ':' + os.environ.get('DB_PW') + '@' + os.environ.get('DB_HOST') + ':5432/' + os.environ.get('DB_NAME'))

'''COL_HEADER_MAPPING = {
    'Bacia': 'strBasin',
    'Campo': 'strField',
    'Estado': 'strState',
    'Contrato': 'strContract',
    'Concessionária ': 'strCompany',
    'Ind. Operadora': 'strOperatortag',
    'Percentual de Participação': 'ParticipationPercentage',
    'Mês': 'Month',
    'Ano': 'Year',
    'Localização (Terra / Mar)' : 'OnoffShore',
    "Lâmina D'Água (m)": 'Waterdepth',
    '°API': 'API',
    'Data Início Produção': 'Productionstartdate',
    'Data Descoberta': 'Discoverydate',
    'Área (Km²)': 'Areasqkm',
    'Vol. Gás Disponível (Mm³)': 'GasavailableMm3',
    'Produção de Petróleo (m³)': 'Petroleumproductionm3',
    'Produção de Óleo (m³)': 'Oilprodm3',
    'Produção de Gás Total (Mm³)': 'TotalgasProdMm3',
    'Produção de Gás Associado (Mm³)': 'AssociatedgasProdMm3',
    'Produção de Gás Não Associado (Mm³)': 'NonassociatedgasprodMm3',
    'Produção de Condensado (m³)': 'Condensateprodm3',
    'Produção de Água (m³)': 'Waterprodm3',
    'Vol. Gás Injetado para Armazenamento (Mm³)': 'InjectedgasstorageMm3',
    'Vol. Queima de Gás (Mm³)': 'FlaredgasMm3',
    'Vol. Gás para Consumo (Mm³)': 'ConsumptiongasMm3',
    'Vol. Gás Royalties (Mm³)': 'RoyaltygasMm3',
    'Vol. Circulação Gás Lift (Mm³)': 'LiftgasMm3',
    'Vol. Gás Injetado Recup. Secundária (Mm³)': 'InjectedgassecondaryrecMm3',
    'Vol. Água Injetado Recup. Secundária (m³)': 'Injectedwatersecondaryrecm3',
    'Vol. Água Injetado Descarte (m³)': 'Injectedwaterdisposalm3',
    'Vol. Água Produzida Descartada (m³)': 'Producedwaterdisposalm3'}'''

COL_HEADER_MAPPING = {
    'Bacia': 'strbasin',
    'Campo': 'strfieldname',
    'Estado': 'strstate',
    'Contrato': 'deccontract',
    'Concessionária ': 'stroperator',
    'Ind. Operadora': 'strisoperator',
    'Percentual de Participação': 'decinterest',
    'Mês': 'decmonth',
    'Ano': 'decyear',
    'Localização (Terra / Mar)' : 'strshorestatus',
    "Lâmina D'Água (m)": 'decwaterdepth',
    '°API': 'decapi',
    'Data Início Produção': 'dteprodstart',
    'Data Descoberta': 'dtediscovery',
    'Área (Km²)': 'decareakm2',
    'Vol. Gás Disponível (Mm³)': 'decgasavailablemm3',
    'Produção de Petróleo (m³)': 'decliquidprodm3',
    'Produção de Óleo (m³)': 'decoilprodm3',
    'Produção de Gás Total (Mm³)': 'dectotalgasprodmm3',
    'Produção de Gás Associado (Mm³)': 'decassocgasprodmm3',
    'Produção de Gás Não Associado (Mm³)': 'decnonassocgasprodmm3',
    'Produção de Condensado (m³)': 'deccondensateprodm3',
    'Produção de Água (m³)': 'decwaterprodm3',
    'Vol. Gás Injetado para Armazenamento (Mm³)': 'decgasinjectionstoragemm3',
    'Vol. Queima de Gás (Mm³)': 'decgasflaredmm3',
    'Vol. Gás para Consumo (Mm³)': 'decgasconsumptionmm3',
    'Vol. Gás Royalties (Mm³)': 'decgasroyaltymm3',
    'Vol. Circulação Gás Lift (Mm³)': 'decgasliftmm3',
    'Vol. Gás Injetado Recup. Secundária (Mm³)': 'decgasinjectionsecondaryrecoverymm3',
    'Vol. Água Injetado Recup. Secundária (m³)': 'decwaterinjectionsecondaryrecoverym3',
    'Vol. Água Injetado Descarte (m³)': 'decwaterinjectiondisposalm3',
    'Vol. Água Produzida Descartada (m³)': 'decwaterproddisposalm3'}

COL_TYPE_MAPPING = {
    'strbasin': str,
    'strfieldname': str,
    'strstate': str,
    'deccontract': str,
    'stroperator': str,
    'strisoperator': str,
    'decinterest': float,
    'decmonth': float,
    'decyear': float,
    'strshorestatus': str,
    'decwaterdepth': float,
    'decapi': float,
    'dteprodstart': str,
    'dtediscovery': str,
    'decareakm2': float,
    'decgasavailablemm3': float,
    'decliquidprodm3': float,
    'decoilprodm3': float,
    'dectotalgasprodmm3': float,
    'decassocgasprodmm3': float,
    'decnonassocgasprodmm3': float,
    'deccondensateprodm3': float,
    'decwaterprodm3': float,
    'decgasinjectionstoragemm3': float,
    'decgasflaredmm3': float,
    'decgasconsumptionmm3': float,
    'decgasroyaltymm3': float,
    'decgasliftmm3': float,
    'decgasinjectionsecondaryrecoverymm3': float,
    'decwaterinjectionsecondaryrecoverym3': float,
    'decwaterinjectiondisposalm3': float,
    'decwaterproddisposalm3': float}

columns_float =['decinterest', 'decmonth' , 'decyear', 'decwaterdepth', 'decapi', 'dteprodstart', 'dtediscovery',
    'decareakm2','decgasavailablemm3', 'decliquidprodm3', 'decoilprodm3', 'dectotalgasprodmm3',
    'decassocgasprodmm3','decnonassocgasprodmm3', 'deccondensateprodm3','decwaterprodm3',
    'decgasinjectionstoragemm3', 'decgasflaredmm3', 'decgasconsumptionmm3', 'decgasroyaltymm3',
    'decgasliftmm3', 'decgasinjectionsecondaryrecoverymm3', 'decwaterinjectionsecondaryrecoverym3',
    'decwaterinjectiondisposalm3', 'decwaterproddisposalm3']

def check_date():
    '''check the last production date of the database'''

    SQL_query_max_date = pd.read_sql_query(
        '''Select max(to_date(decyear || '-' || decmonth || '-01', 'yyyy-dd-mm')) as Run_date
        from "tblFieldProdRaw"''', engine)

    last_date = SQL_query_max_date.iat[0, 0]
    return last_date

def get_content(url, start_date, end_date):
    '''
    make POST request to get the monthly production data
        response specified as XLS ***but*** actual content is HTML
    use BeautifulSoup to extract data from HTML instead of excel

    args:
        url: url to request that generate content
        start_date: start date as mm/yyyy in string format
        end_date: end date as mm/yyyy in string format

    return: in following format (list of dicts)
        [
            {
                col_header_1: val_row_1_col_1,
                col_header_2: val_row_1_col_2,
                col_header_3: val_row_1_col_3,
                ...
            },
            {
                col_header_1: val_row_2_col_1,
                col_header_2: val_row_2_col_2,
                col_header_3: val_row_2_col_3,
                ...
            },
            {
                col_header_1: val_row_3_col_1,
                col_header_2: val_row_3_col_2,
                col_header_3: val_row_3_col_3,
                ...
            },
            ...
        ]
    '''

    # paylo
    payload = {
        'Sim': 'Sim',
        'txtDeOK' : start_date,
        'txtAteOK': end_date
    }

    # verify param suggest requests to NOT validate SSL certificate
    response = requests.post(url, data=payload, verify=False)

    # using BeautifulSoup to parse html is simpler than Excel
    soup = bs(response.content, 'lxml')

    # columns headers are wrapped in B tags
    col_header_elems = soup.find_all('b')
    col_headers = [x.text for x in col_header_elems]

    data = []  # create empty list to store data

    # rows content data are all the TR tags except the first instance
    content_rows = soup.find_all('tr')[1:]

    # iterate content rows
    for row in content_rows:
        # build dictionary for current row
        # by iterate through TD tags in current TR tag
        # key is the col header (get by using index in col_headers)
        # value is text between TD tags and stripped of leading & trailing spaces
        row_data = {
            col_headers[i]: x.text.strip()
            for i, x in enumerate(row.find_all('td'))
        }

        data.append(row_data)  # append data from current row to list

    return data

def parse_df(df):
    df = pd.DataFrame(prod_data)
    df.rename(columns = COL_HEADER_MAPPING,inplace=True)
    df['deccontract'].replace('=TEXTO\\(','',inplace=True, regex=True)
    df['deccontract']= df['deccontract'].str.replace('  ','').str.replace(';"0"\\)','')
    for i in columns_float:
        df[i] = df[i].str.replace(',', '.').str.replace(' ', '')
        df.fillna(0, inplace= True)
    #df = df.astype(COL_TYPE_MAPPING)
    #print(df.dtype)
    return df


def import_to_db(parsed_file):
    ''' check insert dataframe to database '''

    x = df_final.to_sql('tblFieldProdRaw', engine, if_exists='append', index=False, dtype= COL_TYPE_MAPPING)
    print(x)

#    if is True:
#       print('successfully inserted into db')
#    else:
#        print('unable to insert into db')


if __name__ == '__main__':

    months = [str(x).zfill(2) for x in range(1, 13, 1)]
    years = [str(x) for x in range(1998, 2020, 1)]
    dates = []
    for year in years:
        for month in months:
            dates.append(f'{month}/{year}')

    print(dates)

    url = 'https://www.anp.gov.br/SITE/extras/consulta_petroleo_derivados/producao/consultaProdMensalHidrocarbonetos/planilha.asp'

    for date in dates:
        prod_data = get_content(url, date, date)
        if len(prod_data) == 0:
            pass
        df = pd.DataFrame(prod_data)
        #df.to_csv(f'prod{date}.csv', encoding= 'utf-8-sig')

        df_final = parse_df(prod_data)
        df_final.to_csv(f"prod-{date.replace('/', '-')}.csv", encoding = 'utf-8-sig')
