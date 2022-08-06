import pandas as pd
from pathlib import Path


def runtreat():

    basepath = Path('.') / 'Main' / 'database'
    tempospath = basepath / 'raw' / 'Atr_tempos'
    atr_infopath = basepath / 'raw' / 'Atr_info'

    print(tempospath)

    atr_tempos = {}

    #tempos_header = ['IDAtracacao', 'TEsperaAtracacao', 'TEsperaInicioOp',
    #                 'TOperacao', 'TEsperaDesatracacao', 'TAtracado',
    #                 'TEstadia']

    for y in range(2020, 2023):

        atr_tempos[y] = pd.read_csv(tempospath / f'{y}TemposAtracacao.txt', delimiter=";", decimal=",",
                                    encoding='utf-8-sig',
                                    dtype={'IDAtracacao': int,
                                           'TEsperaAtracacao': float,
                                           'TEsperaInicioOp': float,
                                           'TOperacao': float,
                                           'TEsperaDesatracacao': float,
                                           'TAtracado': float,
                                           'TEstadia': float})

        atr_tempos['Ano'] = y

        print(y)

    print('df_tempos read')
    #print(atr_tempos[2010][0:5])

    atr_info = {}

    for y in range(2020, 2023):

        atr_info[y] = pd.read_csv(atr_infopath / f'{y}Atracacao.csv',
                                      sep=';',
                                      encoding='utf8',
                                      dtype={'IDAtracacao':int,
                                             'CDTUP':str,
                                             'IDBerco':str,
                                             'Berço':str,
                                             'Porto Atracação':str,
                                             'Apelido Instalação Portuária':str,
                                             'Complexo Portuário':str,
                                             'Tipo da Autoridade Portuária':str,
                                             'Data Atracação':str,
                                             'Data Chegada':str,
                                             'Data Desatracação':str,
                                             'Data Início Operação':str,
                                             'Data Término Operação':str,
                                             'Ano':str,
                                             'Mes':str,
                                             'Tipo de Operação':str,
                                             'Tipo de Navegação da Atracação':str,
                                             'Nacionalidade do Armador':str,
                                             'FlagMCOperacaoAtracacao':str,
                                             'Terminal':str,
                                             'Município':str,
                                             'UF':str,
                                             'SGUF':str,
                                             'Região Geográfica':str,
                                             'NdaCapitania':str,
                                             'Nº do IM':int})
        print(y)

    print('df_atrinfo read')

    all_atr = {}
    for y in range(2020, 2023):

        all_atr[y] = pd.merge(atr_tempos[y],
                              atr_info[y],
                              on='IDAtracacao')
        print(f'merged year {y}')


    df_full_atr = pd.DataFrame()

    for y in range(2020, 2023):

        df_full_atr = df_full_atr.append(all_atr[y])

        print(f'appended year {y}')

    print('saving dataframe full')

    df_full_atr.to_csv(basepath / 'raw' / 'full_atr.csv', sep=',', encoding='utf-8', index=False)
