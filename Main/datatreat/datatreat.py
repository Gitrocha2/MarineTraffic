import pandas as pd
from pathlib import Path


basepath = Path('.') / 'Main' / 'database'
tempospath = basepath / 'raw' / 'Atr_tempos'
atr_infopath = basepath / 'raw' / 'Atr_info'

print(tempospath)

atr_tempos = {}

for y in range(2010, 2020):

    atr_tempos[y] = pd.read_csv(tempospath / f'{y}TemposAtracacao.txt',
                                sep=';', encoding='cp1252',
                                dtype={'IDAtracacao': int,
                                       'TEsperaAtracacao': float,
                                       'TEsperaInicioOp': float,
                                       'TOperacao': float,
                                       'TEsperaDesatracacao': float,
                                       'TAtracado': float,
                                       'TEstadia': float,
                                       'Ano': int})
    print(y)

print('df_tempos read')
#print(atr_tempos[2010][0:5])

atr_info = {}

for y in range(2010, 2020):

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
                                         'Nº da Capitania':str,
                                         'Nº do IM':int})
    print(y)

print('df_atrinfo read')
#print(atr_info[2010][0:5])

all_atr = {}
for y in range(2010, 2020):

    all_atr[y] = pd.merge(atr_tempos[y],
                          atr_info[y],
                          on='IDAtracacao')
    print(f'merged year {y}')


df_full_atr = pd.DataFrame()

for y in range(2010, 2020):

    df_full_atr = df_full_atr.append(all_atr[y])

    print(f'appended year {y}')

print('saving dataframe full')
df_full_atr.to_csv(basepath / 'raw' / 'full_atr.csv', sep=',', encoding='utf-8', index=False)
