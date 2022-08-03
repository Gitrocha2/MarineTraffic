from Main.database import connectors
import sqlite3
import time as t
import pandas as pd
from pathlib import Path
import sys
from os import mkdir
from Main.analysis import metrics, profile_generator
from functools import reduce


# Single query in DB
def print_exception():
    import linecache
    import sys
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    message = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    return message


def loads_query(list):

    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    result = connectors.find_load_exact(loadid=list, connection=conn)

    #print('result sliced', str(result)[0:100], 'result msg:', result['Message'], '\n\n', 'type', type(result))

    if result['Status'] == 0:
        print('Empty Result for the loads searched.')
        return pd.DataFrame()

    df_trips = pd.DataFrame(result['Message'], columns=["IDCarga",
                                                        "IDAtracacao",
                                                        "Origem",
                                                        "Destino",
                                                        "CDMercadoria",
                                                        "Tipo Operação da Carga",
                                                        "Carga Geral Acondicionamento",
                                                        "ConteinerEstado",
                                                        "Tipo Navegação",
                                                        "FlagAutorizacao",
                                                        "FlagCabotagem",
                                                        "FlagCabotagemMovimentacao",
                                                        "FlagConteinerTamanho",
                                                        "FlagLongoCurso",
                                                        "FlagMCOperacaoCarga",
                                                        "FlagOffshore",
                                                        "FlagTransporteViaInterioir",
                                                        "Percurso Transporte em vias Interiores",
                                                        "Percurso Transporte Interiores",
                                                        "STNaturezaCarga",
                                                        "STSH2",
                                                        "STSH4",
                                                        "Natureza da Carga",
                                                        "Sentido",
                                                        "TEU",
                                                        "QTCarga",
                                                        "VLPesoCargaBruta",
                                                        "CDMercadoriaConteinerizada",
                                                        "VLPesoCargaCont"])

    return df_trips


def imo_query(nimo):

    #try:
    #    nimo = int(input('\n Insira o Número IMO para gerar relatório (Ou zero para outras consultas): '))
    #except:
    #    print('\n Entrada inválida, digite o número IMO apenas.')
    #    return 's'

    print('\n Salvando dados...')

    x = t.time()
    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    if nimo == 0:
        print('Pesquisando IMO 0')
        result = connectors.find_imo_blank(connection=conn)
    else:
        result = connectors.find_imo_exact(imo=nimo, connection=conn)
    conn.close()
    y = t.time()

    if isinstance(result['Message'], str):
        print('string message in nimo quero')
        print('Result Message: \n', str(result['Message'])[0:100] )
        return 400

    else:

        print('\n Organizando diretórios.')
        try:
            basepath = Path('.') / 'Reports' / f'IMO-{nimo}'
            mkdir(basepath)
            mkdir(basepath / 'viagens')
            mkdir(basepath / 'cargas')
        except:
            print('\n Pasta Já existe')
            return 'n'

        df_trips = pd.DataFrame(result['Message'], columns=["IDAtracacao",
                                                            "TEsperaAtracacao",
                                                            "TEsperaInicioOp",
                                                            "TOperacao",
                                                            "TEsperaDesatracacao",
                                                            "TAtracado",
                                                            "TEstadia",
                                                            "CDTUP",
                                                            "IDBerco",
                                                            "Berco",
                                                            "PortoAtracacao",
                                                            "ApelidoInstalacaoPortuaria",
                                                            "ComplexoPortuario",
                                                            "TipodaAutoridadePortuaria",
                                                            "DataAtracacao",
                                                            "DataChegada",
                                                            "DataDesatracacao",
                                                            "DataInicioOperacao",
                                                            "DataTerminoOperacao",
                                                            "Ano",
                                                            "Mes",
                                                            "TipodeOperacao",
                                                            "TipodeNavegacaodaAtracacao",
                                                            "NacionalidadedoArmador",
                                                            "FlagMCOperacaoAtracacao",
                                                            "Terminal",
                                                            "Municipio",
                                                            "UF",
                                                            "SGUF",
                                                            "RegiaoGeografica",
                                                            "NdaCapitania",
                                                            "NdoIMO"])

        # ----------- Create report metrics ---------------------------------
        df_trips = df_trips[["IDAtracacao",
                             "TEsperaAtracacao",
                             "TEsperaInicioOp",
                             "TOperacao",
                             "TEsperaDesatracacao",
                             "TAtracado",
                             "TEstadia",
                             "PortoAtracacao",
                             "DataAtracacao",
                             "DataChegada",
                             "DataDesatracacao",
                             "DataInicioOperacao",
                             "DataTerminoOperacao",
                             "TipodeOperacao",
                             "TipodeNavegacaodaAtracacao",
                             "SGUF",
                             "NdaCapitania",
                             "NdoIMO"]]

        df_trips = df_trips.rename(columns={
            'PortoAtracacao': "Porto",
            'DataAtracacao': 'Atracado',
            'DataChegada': 'Chegada',
            'DataDesatracacao': 'Desatracado',
            'DataInicioOperacao': 'InicioOp',
            'DataTerminoOperacao': 'FimOp',
            'TipodeNavegacaodaAtracacao': 'TipoNav',
            'SGUF': 'UF',
            'NdaCapitania': 'Capitania',
            'NdoIMO': 'IMO'})

        df_trips = df_trips.astype({'IDAtracacao': str,
                                    'TEsperaAtracacao': float,
                                    'TEsperaInicioOp': float,
                                    'TOperacao': float,
                                    'TEsperaDesatracacao': float,
                                    'TAtracado': float,
                                    'TEstadia': float,
                                    'Porto': str,
                                    'Atracado': str,
                                    'Chegada': str,
                                    'Desatracado': str,
                                    'InicioOp': str,
                                    'FimOp': str,
                                    'TipoNav': str,
                                    'UF': str,
                                    'Capitania': str,
                                    'IMO': int})

        prancha = 0
        tope = 1
        tatr = 2
        tesp = 3
        vmed = 4
        load = 5

        filename = basepath / 'resumo.txt'
        with open(filename, 'w+') as reports:
            reports.write(f'Prancha média: {prancha}\n')
            reports.write(f'Tempo médio de operação: {tope}\n')
            reports.write(f'Tempo médio de atracação: {tatr}\n')
            reports.write(f'Tempo médio de espera: {tesp}\n')
            reports.write(f'Velocidade média: {vmed}\n')
            reports.write(f'Carga média transportada: {load}\n')

        # ----------- Loads report generation -------------------------------

        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')

        df_aux = df_trips['IDAtracacao'].copy(deep=True)

        df = df_aux.drop_duplicates(keep='first')

        idatr_list = df.values.tolist()

        u = t.time()
        print('idatr list', idatr_list)

        df_loads = loads_query(list=idatr_list)

        #if df_loads.empty:
        #    return 's'

        v = t.time()

        # -------------- Saving DFs to disk ------------------------

        df_trips.to_csv(basepath / 'viagens' / f'Viagens-{nimo}.csv', sep=';', encoding='cp1252', index=False)
        df_loads.to_csv(basepath / 'cargas' / f'Cargas-{nimo}.csv', sep=';', encoding='cp1252', index=False)
        print('\n Finalizado. Tempo total de consulta IMO = ', round((y-x), 2), 'segundos')
        print('\n Tempo total de consulta de viagens = ', round((v - u), 2), 'segundos')
        #rerun = input('\pe[0n Deseja consultar novamente? (S ou N):  ').lower()
        trips_found = df_trips.shape[0]
        loads_found = df_loads.shape[0]

        print('Trips found: ', trips_found, 'Loads movements :', loads_found)

        if (trips_found > 0):
            return 200
        else:
            return 400



def imolist_query(nimo, name, amode):


    # System Inputs

    #try:
    #    nimo = input('\n Insira os Números IMO, separados por vírgula, para gerar relatório (Ou zero para outras consultas): ')
    #except:
    #    print('\n Entrada inválida, digite o número IMO apenas.')
    #    return 's'

    print('\n Salvando dados...')

    # System Query

    x = t.time()
    conn = sqlite3.connect('./Main/database/data/atr_info.db')

    if nimo == 0:
        result = connectors.find_imo_blank(connection=conn)
    else:
        print(nimo)
        result = connectors.find_imolist_exact(imolist=nimo, connection=conn)
        #{'Status': 'ok', 'Message': result}

    conn.close()
    y = t.time()

    # System Reports

    if isinstance(result['Message'], str):
        # {'Status': 'ok', 'Message': 'Ship not found'}
        #print('Result Message: \n', result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        # {'Status': 'ok', 'Message': [List of ships]}
        # Load json in Pandas DF
        df_trips = pd.DataFrame(result['Message'], columns=["IDAtracacao",
                                                            "TEsperaAtracacao",
                                                            "TEsperaInicioOp",
                                                            "TOperacao",
                                                            "TEsperaDesatracacao",
                                                            "TAtracado",
                                                            "TEstadia",
                                                            "CDTUP",
                                                            "IDBerco",
                                                            "Berco",
                                                            "PortoAtracacao",
                                                            "ApelidoInstalacaoPortuaria",
                                                            "ComplexoPortuario",
                                                            "TipodaAutoridadePortuaria",
                                                            "DataAtracacao",
                                                            "DataChegada",
                                                            "DataDesatracacao",
                                                            "DataInicioOperacao",
                                                            "DataTerminoOperacao",
                                                            "Ano",
                                                            "Mes",
                                                            "TipodeOperacao",
                                                            "TipodeNavegacaodaAtracacao",
                                                            "NacionalidadedoArmador",
                                                            "FlagMCOperacaoAtracacao",
                                                            "Terminal",
                                                            "Municipio",
                                                            "UF",
                                                            "SGUF",
                                                            "RegiaoGeografica",
                                                            "NdaCapitania",
                                                            "NdoIMO"])

        # ----------- Create report metrics ---------------------------------
        # Slice dataframe columns
        df_trips = df_trips[["IDAtracacao",
                             "TEsperaAtracacao",
                             "TEsperaInicioOp",
                             "TOperacao",
                             "TEsperaDesatracacao",
                             "TAtracado",
                             "TEstadia",
                             "PortoAtracacao",
                             "DataAtracacao",
                             "DataChegada",
                             "DataDesatracacao",
                             "DataInicioOperacao",
                             "DataTerminoOperacao",
                             "TipodeOperacao",
                             "TipodeNavegacaodaAtracacao",
                             "SGUF",
                             "NdaCapitania",
                             "NdoIMO"]]
        df_trips = df_trips.rename(columns={
            'PortoAtracacao': "Porto",
            'DataAtracacao': 'Atracado',
            'DataChegada': 'Chegada',
            'DataDesatracacao': 'Desatracado',
            'DataInicioOperacao': 'InicioOp',
            'DataTerminoOperacao': 'FimOp',
            'TipodeNavegacaodaAtracacao': 'TipoNav',
            'SGUF': 'UF',
            'NdaCapitania': 'Capitania',
            'NdoIMO': 'IMO'})

        print(df_trips.head(3))

        #df_trips.to_csv('./teste_csv')
        # Set datatypes of df columns
        df_trips = df_trips.astype({'IDAtracacao': int,
                                    'TEsperaAtracacao': float,
                                    'TEsperaInicioOp': float,
                                    'TOperacao': float,
                                    'TEsperaDesatracacao': float,
                                    'TAtracado': float,
                                    'TEstadia': float,
                                    'Porto': str,
                                    'Atracado': str,
                                    'Chegada': str,
                                    'Desatracado': str,
                                    'InicioOp': str,
                                    'FimOp': str,
                                    'TipoNav': str,
                                    'UF': str,
                                    'Capitania': str})
        # Collect report metrics
        # tespatr = round(df_trips['TEsperaAtracacao'].mean(), 2)
        # tespop = round(df_trips['TEsperaInicioOp'].mean(), 2)
        # tope = round(df_trips['TOperacao'].mean(), 2)
        # tatr = round(df_trips['TAtracado'].mean(), 2)
        # tespdatr = round(df_trips['TEsperaDesatracacao'].mean(), 2)
        # testad = round(df_trips['TEstadia'].mean(), 2)

        # ----------- Loads report generation -------------------------------
        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')
        # Add later - generate loads tables
        df_aux = df_trips['IDAtracacao'].copy(deep=True)
        df = df_aux.drop_duplicates(keep='first')
        idatr_list = df.values.tolist()
        # Run query of loads from shiplist history
        print(' List of trips generated. Searching trips in database.')
        u = t.time()
        df_loads = loads_query(list=idatr_list)
        v = t.time()
        print(' Query finished.')
        # Slice loads dataframe columns
        df_loads = df_loads[['IDCarga',
                             'IDAtracacao',
                             'Origem',
                             'Destino',
                             'Tipo Operação da Carga',
                             'Natureza da Carga',
                             'Sentido',
                             'TEU',
                             'QTCarga',
                             'VLPesoCargaBruta',
                             'CDMercadoriaConteinerizada',
                             'VLPesoCargaCont']]

        if amode == 'teu':
            df_loads = df_loads.drop_duplicates(subset='IDCarga', keep="first")

        df_loads.to_csv(Path('.') / 'Reports' / 'Fleets' / f'Cargas2.csv',
                        sep=';',
                        encoding='cp1252', index=False)

        df_loads['TEU'] = df_loads['TEU'].astype(str)
        df_loads['TEU'] = df_loads['TEU'].str.replace(',', '.').astype(float).round(0)

        # Set loads df datatypes
        df_loads = df_loads.astype({'IDCarga': str,
                                    'IDAtracacao': int,
                                    'Origem': str,
                                    'Destino': str,
                                    'Tipo Operação da Carga': str,
                                    'Natureza da Carga': str,
                                    'Sentido': str,
                                    'TEU': int,
                                    'QTCarga': int,
                                    'VLPesoCargaBruta': float,
                                    'CDMercadoriaConteinerizada': str,
                                    'VLPesoCargaCont': str})

        # -------------- Create merged DF -----------
        # TODO: Add more slices to improve analysis stats
        df_loads_slice = df_loads[['IDAtracacao', 'Sentido', 'TEU']]

        df_movs_group = df_loads_slice.groupby(['Sentido'])

        # Load Aggregation
        df_list = []
        df_list.append(df_trips)
        # TEUs Aggregation
        try:
            df_teus_in = df_movs_group.get_group('Embarcados')
            df_teus_in = df_teus_in[['IDAtracacao', 'TEU']]
            df_teus_in_agg = df_teus_in.groupby(['IDAtracacao']).agg({'TEU': ['sum']})
            df_teus_in_agg = df_teus_in_agg.reset_index()
            df_teus_in_agg.columns = ['IDAtracacao', 'TEUs_IN']
            df_list.append(df_teus_in_agg)
            teus_in = True
        except:
            print(' Não há cargas embarcadas')
            teus_in = False

        try:
            df_teus_out = df_movs_group.get_group('Desembarcados')
            df_teus_out = df_teus_out[['IDAtracacao', 'TEU']]
            df_teus_out_agg = df_teus_out.groupby(['IDAtracacao']).agg({'TEU': ['sum']})
            df_teus_out_agg = df_teus_out_agg.reset_index()
            df_teus_out_agg.columns = ['IDAtracacao', 'TEUs_OUT']
            df_list.append(df_teus_out_agg)
            teus_out = True
        except:
            print(' Não há cargas desembarcadas')
            teus_out = False

        print(' Creating final report.')
        result_merge = reduce(lambda left, right: pd.merge(left, right, on='IDAtracacao', how='outer'), df_list)

        if not teus_in:
            result_merge['TEUs_IN'] = 0
        if not teus_out:
            result_merge['TEUs_OUT'] = 0

        basepath = Path('.') / 'Reports' / 'Fleets' / f'{amode}_Fleet-{name}'

        print(' Organizando diretório de viagens.')
        try:
            mkdir(basepath)
            mkdir(basepath / 'viagens')
            #plt.savefig(basepath / f'Prancha-Hist-{name}.png')
            #df_trips.to_csv(basepath / 'viagens' / f'Viagens-{nimo}.csv', sep=';', encoding='cp1252', index=False)
            result_merge.to_csv(basepath / 'viagens' / f'Resultado.csv', sep=';', encoding='cp1252', index=False)
        except:
            print('Pasta Já existe')
            return 'n'
        print(' Organizando diretório de cargas.')
        try:
            mkdir(basepath / 'cargas')
            df_loads.to_csv(basepath / 'cargas' / f'Cargas.csv', sep=';', encoding='cp1252', index=False)
        except:
            print('Pasta Já existe')
            return 's'

        # -------------- Saving reports to disk -----------

        print('\n Finalizado. Tempo total de consulta IMO = ', round((y-x), 2), 'segundos')
        print('\n Tempo total de consulta de viagens = ', round((v - u), 2), 'segundos')
        # rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        #return rerun


def research_query(month, year):

    print('\n Salvando dados...')

    # System Query

    x = t.time()
    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    print('Date searched', month, '/', year)
    #result = connectors.find_trips_mmyyyy(month=month, year=month, connection=conn)
    result = connectors.find_trips_mmyyyy(month=month, year=year, connection=conn)
    # {'Status': 'ok', 'Message': result}

    conn.close()
    y = t.time()

    # System Reports

    if isinstance(result['Message'], str):
        # {'Status': 'ok', 'Message': 'Ship not found'}
        print('Result Message: \n', result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        # {'Status': 'ok', 'Message': [List of ships]}
        # Load json in Pandas DF
        df_trips = pd.DataFrame(result['Message'], columns=["IDAtracacao",
                                                            "TEsperaAtracacao",
                                                            "TEsperaInicioOp",
                                                            "TOperacao",
                                                            "TEsperaDesatracacao",
                                                            "TAtracado",
                                                            "TEstadia",
                                                            "CDTUP",
                                                            "IDBerco",
                                                            "Berco",
                                                            "PortoAtracacao",
                                                            "ApelidoInstalacaoPortuaria",
                                                            "ComplexoPortuario",
                                                            "TipodaAutoridadePortuaria",
                                                            "DataAtracacao",
                                                            "DataChegada",
                                                            "DataDesatracacao",
                                                            "DataInicioOperacao",
                                                            "DataTerminoOperacao",
                                                            "Ano",
                                                            "Mes",
                                                            "TipodeOperacao",
                                                            "TipodeNavegacaodaAtracacao",
                                                            "NacionalidadedoArmador",
                                                            "FlagMCOperacaoAtracacao",
                                                            "Terminal",
                                                            "Municipio",
                                                            "UF",
                                                            "SGUF",
                                                            "RegiaoGeografica",
                                                            "NdaCapitania",
                                                            "NdoIMO"])

        # ----------- Create report metrics ---------------------------------
        # Slice dataframe columns
        df_trips = df_trips[["IDAtracacao",
                             "TEsperaAtracacao",
                             "TEsperaInicioOp",
                             "TOperacao",
                             "TEsperaDesatracacao",
                             "TAtracado",
                             "TEstadia",
                             "PortoAtracacao",
                             "DataAtracacao",
                             "DataChegada",
                             "DataDesatracacao",
                             "DataInicioOperacao",
                             "DataTerminoOperacao",
                             "TipodeOperacao",
                             "TipodeNavegacaodaAtracacao",
                             "SGUF",
                             "NdaCapitania",
                             "NdoIMO"]]
        df_trips = df_trips.rename(columns={
            'PortoAtracacao': "Porto",
            'DataAtracacao': 'Atracado',
            'DataChegada': 'Chegada',
            'DataDesatracacao': 'Desatracado',
            'DataInicioOperacao': 'InicioOp',
            'DataTerminoOperacao': 'FimOp',
            'TipodeNavegacaodaAtracacao': 'TipoNav',
            'SGUF': 'UF',
            'NdaCapitania': 'Capitania',
            'NdoIMO': 'IMO'})

        df_trips.loc[(df_trips.IMO == ''), 'IMO'] = 0

        # Set datatypes of df columns
        df_trips = df_trips.astype({'IDAtracacao': int,
                                    'TEsperaAtracacao': float,
                                    'TEsperaInicioOp': float,
                                    'TOperacao': float,
                                    'TEsperaDesatracacao': float,
                                    'TAtracado': float,
                                    'TEstadia': float,
                                    'Porto': str,
                                    'Atracado': str,
                                    'Chegada': str,
                                    'Desatracado': str,
                                    'InicioOp': str,
                                    'FimOp': str,
                                    'TipoNav': str,
                                    'UF': str,
                                    'Capitania': str,
                                    'IMO': int})

        # ----------- Loads report generation -------------------------------
        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')
        # Add later - generate loads tables
        df_aux = df_trips['IDAtracacao'].copy(deep=True)
        df = df_aux.drop_duplicates(keep='first')
        idatr_list = df.values.tolist()
        # Run query of loads from shiplist history
        print(' List of trips generated. Searching trips in database.')
        u = t.time()
        df_loads = loads_query(list=idatr_list)
        v = t.time()
        print(' Query finished.')
        # Slice loads dataframe columns
        df_loads = df_loads[['IDCarga',
                             'IDAtracacao',
                             'Origem',
                             'Destino',
                             'Tipo Operação da Carga',
                             'Natureza da Carga',
                             'Sentido',
                             'TEU',
                             'QTCarga',
                             'VLPesoCargaBruta',
                             'CDMercadoriaConteinerizada',
                             'VLPesoCargaCont']]
        # Set loads df datatypes
        # TODO: Replace comma to convert to int and float
        df_loads = df_loads.astype({'IDCarga': str,
                                    'IDAtracacao': int,
                                    'Origem': str,
                                    'Destino': str,
                                    'Tipo Operação da Carga': str,
                                    'Natureza da Carga': str,
                                    'Sentido': str,
                                    'TEU': int,
                                    'QTCarga': int,
                                    'VLPesoCargaBruta': float,
                                    'CDMercadoriaConteinerizada': str,
                                    'VLPesoCargaCont': str})

        # -------------- Create merged DF -----------
        # TODO: Add more slices to improve analysis stats
        df_loads_slice = df_loads[['IDAtracacao', 'Sentido', 'VLPesoCargaBruta']]

        df_loads_group = df_loads_slice.groupby(['Sentido'])
        df_loads_in = df_loads_group.get_group('Embarcados')
        df_loads_in = df_loads_in[['IDAtracacao', 'VLPesoCargaBruta']]
        df_loads_in_agg = df_loads_in.groupby(['IDAtracacao']).agg({'VLPesoCargaBruta': ['sum']})
        df_loads_in_agg = df_loads_in_agg.reset_index()
        df_loads_in_agg.columns = ['IDAtracacao', 'VLPesoCargaBruta_IN']
        #print(df_loads_in_agg)

        df_loads_group = df_loads_slice.groupby(['Sentido'])
        df_loads_out = df_loads_group.get_group('Desembarcados')
        df_loads_out = df_loads_out[['IDAtracacao', 'VLPesoCargaBruta']]
        df_loads_out_agg = df_loads_out.groupby(['IDAtracacao']).agg({'VLPesoCargaBruta': ['sum']})
        df_loads_out_agg = df_loads_out_agg.reset_index()
        df_loads_out_agg.columns = ['IDAtracacao', 'VLPesoCargaBruta_OUT']
        #print(df_loads_out_agg)

        print(' Creating final report.')
        df_list = [df_trips, df_loads_in_agg, df_loads_out_agg]
        result_merge = reduce(lambda left, right: pd.merge(left, right, on='IDAtracacao', how='outer'), df_list)

        basepath = Path('.') / 'Reports' / 'Research' / f'{year}-{month}'

        print(' Organizando diretórios.')
        try:
            mkdir(basepath)
            mkdir(basepath / 'viagens')
        except:
            print('Pasta já existe')
        result_merge.to_csv(basepath / 'viagens' / f'Resultado.csv', sep=';', encoding='cp1252', index=False)
        try:
            mkdir(basepath / 'cargas')
            df_loads.to_csv(basepath / 'cargas' / f'Cargas.csv', sep=';', encoding='cp1252', index=False)
        except:
            print('Pasta Já existe')
            return 's'

        # -------------- Saving reports to disk -----------

        print('\n Finalizado. Tempo total de consulta IMO = ', round((y - x), 2), 'segundos')
        print('\n Tempo total de consulta de viagens = ', round((v - u), 2), 'segundos')


def cap_query():

    conn = sqlite3.connect('./Main/database/data/atr_info.db')

    try:
        nimo = int(input('\n Insira o Número da Capitania para gerar relatório (Ou zero para outras consultas): '))
    except:
        print('\n Entrada inválida, digite o número da Capitania apenas.')
        return 's'

    x = t.time()
    if nimo == 0:
        result = connectors.find_imo_blank(connection=conn)
    else:
        result = connectors.find_imo_exact(imo=nimo, connection=conn)
    y = t.time()
    conn.close()

    if isinstance(result['Message'], str):
        print(result['Message'])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        print('\n Consulta concluída...')
        df_teste = pd.DataFrame(result['Message'], columns=["IDAtracacao",
                                                            "TEsperaAtracacao",
                                                            "TEsperaInicioOp",
                                                            "TOperacao",
                                                            "TEsperaDesatracacao",
                                                            "TAtracado",
                                                            "TEstadia",
                                                            "CDTUP",
                                                            "IDBerco",
                                                            "Berco",
                                                            "PortoAtracacao",
                                                            "ApelidoInstalacaoPortuaria",
                                                            "ComplexoPortuario",
                                                            "TipodaAutoridadePortuaria",
                                                            "DataAtracacao",
                                                            "DataChegada",
                                                            "DataDesatracacao",
                                                            "DataInicioOperacao",
                                                            "DataTerminoOperacao",
                                                            "Ano",
                                                            "Mes",
                                                            "TipodeOperacao",
                                                            "TipodeNavegacaodaAtracacao",
                                                            "NacionalidadedoArmador",
                                                            "FlagMCOperacaoAtracacao",
                                                            "Terminal",
                                                            "Municipio",
                                                            "UF",
                                                            "SGUF",
                                                            "RegiaoGeografica",
                                                            "NdaCapitania",
                                                            "NdoIMO"])

        # print(df_test[0:5])

        basepath = Path('.') / 'Reports' / 'viagens'

        print('\n Salvando dados...')
        df_teste.to_csv(basepath / f'viagens_CAPT-{nimo}.csv', sep=';', encoding='cp1252', index=False)

        print('\n Finalizado. Tempo total de consulta = ', round((y-x), 2), 'segundos')

        rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        return rerun


def ploads_query():

    try:
        codport = str(input('\n Insira o código do porto para gerar relatório): '))
    except:
        print('\n Entrada inválida, digite o código do porto apenas.')
        return 's'

    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    basepath = Path('.') / 'Reports' / f'Porto-{codport}'

    x = t.time()
    if codport == 0:
        return 'n'
    else:
        result = connectors.find_port_loads(portid=codport, connection=conn)
    y = t.time()
    conn.close()

    if isinstance(result['Message'], str):
        print('sliced find port loads', str(result['Message'])[0:100])
        rerun = input('Deseja consultar novamente? (S ou N): ').lower()
        return rerun

    else:
        print('\n Consulta de navio concluída. Iniciando consulta por cargas...')
        df_trips = pd.DataFrame(result['Message'], columns=["IDCarga",
                                                            "IDAtracacao",
                                                            "Origem",
                                                            "Destino",
                                                            "CDMercadoria",
                                                            "Tipo Operação da Carga",
                                                            "Carga Geral Acondicionamento",
                                                            "ConteinerEstado",
                                                            "Tipo Navegação",
                                                            "FlagAutorizacao",
                                                            "FlagCabotagem",
                                                            "FlagCabotagemMovimentacao",
                                                            "FlagConteinerTamanho",
                                                            "FlagLongoCurso",
                                                            "FlagMCOperacaoCarga",
                                                            "FlagOffshore",
                                                            "FlagTransporteViaInterioir",
                                                            "Percurso Transporte em vias Interiores",
                                                            "Percurso Transporte Interiores",
                                                            "STNaturezaCarga",
                                                            "STSH2",
                                                            "STSH4",
                                                            "Natureza da Carga",
                                                            "Sentido",
                                                            "TEU",
                                                            "QTCarga",
                                                            "VLPesoCargaBruta",
                                                            "CDMercadoriaConteinerizada",
                                                            "VLPesoCargaCont"])


        try:
            mkdir(basepath)

        except:
            print('Pasta Já existe')
            return 's'

        print('\n Salvando dados...')

        df_trips.to_csv(basepath / f'Movimentos-{codport}.csv', sep=';', encoding='cp1252', index=False)
        print('\n Finalizado. Tempo total de consulta de movimentos de cargas = ', round((y-x), 2), 'segundos')
        rerun = input('\n Deseja consultar novamente? (S ou N):  ').lower()
        return rerun


def pship_query():
    return True


def find_ships():

    atr_file = Path('..') / 'Inputs' / 'oil_trips.csv'
    print(atr_file)
    atr_df = pd.read_csv(atr_file)
    print(atr_df.head())
    atr_list = atr_df['IDAtracacao'].tolist()

    atr_sliced = [atr_list[i:i+300] for i in range(0, len(atr_list), 300)]
    print('\n Salvando dados...')

    # System Query
    conn = sqlite3.connect('./database/data/atr_info.db')

    counter = 0
    df_list = []
    for group in atr_sliced:
        result = connectors.find_ships_by_trips(imolist=group, connection=conn)

        # System Reports
        if isinstance(result['Message'], str):
            # {'Status': 'ok', 'Message': 'Ship not found'}
            print('Result Message: \n', result['Message'])
            rerun = input('Deseja consultar novamente? (S ou N): ').lower()
            return rerun
        else:
            # {'Status': 'ok', 'Message': [List of ships]}
            # Load json in Pandas DF
            df_trips = pd.DataFrame(result['Message'], columns=["IDAtracacao",
                                                                "TEsperaAtracacao",
                                                                "TEsperaInicioOp",
                                                                "TOperacao",
                                                                "TEsperaDesatracacao",
                                                                "TAtracado",
                                                                "TEstadia",
                                                                "CDTUP",
                                                                "IDBerco",
                                                                "Berco",
                                                                "PortoAtracacao",
                                                                "ApelidoInstalacaoPortuaria",
                                                                "ComplexoPortuario",
                                                                "TipodaAutoridadePortuaria",
                                                                "DataAtracacao",
                                                                "DataChegada",
                                                                "DataDesatracacao",
                                                                "DataInicioOperacao",
                                                                "DataTerminoOperacao",
                                                                "Ano",
                                                                "Mes",
                                                                "TipodeOperacao",
                                                                "TipodeNavegacaodaAtracacao",
                                                                "NacionalidadedoArmador",
                                                                "FlagMCOperacaoAtracacao",
                                                                "Terminal",
                                                                "Municipio",
                                                                "UF",
                                                                "SGUF",
                                                                "RegiaoGeografica",
                                                                "NdaCapitania",
                                                                "NdoIMO"])

            # ----------- Create report metrics ---------------------------------
            # Slice dataframe columns
            df_trips = df_trips[["IDAtracacao",
                                 "TEsperaAtracacao",
                                 "TEsperaInicioOp",
                                 "TOperacao",
                                 "TEsperaDesatracacao",
                                 "TAtracado",
                                 "TEstadia",
                                 "PortoAtracacao",
                                 "DataAtracacao",
                                 "DataChegada",
                                 "DataDesatracacao",
                                 "DataInicioOperacao",
                                 "DataTerminoOperacao",
                                 "TipodeOperacao",
                                 "TipodeNavegacaodaAtracacao",
                                 "SGUF",
                                 "NdaCapitania",
                                 "NdoIMO"]]

            df_trips = df_trips.rename(columns={
                'PortoAtracacao': "Porto",
                'DataAtracacao': 'Atracado',
                'DataChegada': 'Chegada',
                'DataDesatracacao': 'Desatracado',
                'DataInicioOperacao': 'InicioOp',
                'DataTerminoOperacao': 'FimOp',
                'TipodeNavegacaodaAtracacao': 'TipoNav',
                'SGUF': 'UF',
                'NdaCapitania': 'Capitania',
                'NdoIMO': 'IMO'})
            # Set datatypes of df columns
            #filename = Path('.') / 'analysis' / 'Tankers' / f'tankers_trips_{counter}-300.csv'
            df_list.append(df_trips)
            #df_trips.to_csv(filename, sep=';', index=False, encoding='cp1252')
            print(counter)
            counter += 300

    conn.close()
    final_df = reduce(lambda left, right: pd.concat([left, right], axis=0, sort=False), df_list)
    final_df.to_csv(Path('.') / 'analysis' / 'Tankers' / f'tankers_trips_{counter}-300.csv', sep=';', encoding='cp1252', index=False)


# Multiple Queries iterators
def imo_multilist_query(amode):

    with open(Path('Inputs') / 'fleets.txt', 'r') as inputfile:
        list_of_groups = []
        group_names = []
        for line in inputfile:
            #print('line:', line)
            split = line.split(';', 1)
            #print('split:', split)

            header = split[0]
            #print('header:', header)
            group_names.append(header)
            tail = split[1]
            #print('tail:', tail)
            list_of_groups.append(tail)

    print('tails', list_of_groups)
    print('headers', group_names)

    list_of_groups = [list.replace('\n', '') for list in list_of_groups]

    print('tails clean', list_of_groups)

    xid = 0
    iters = len(group_names)
    for group in range(iters):

        imo = list_of_groups[xid]
        print(imo)
        name = group_names[xid]
        print(name)
        imolist_query(nimo=imo, name=name, amode=amode)
        xid += 1

    return True


def multi_research_query(years):

    #list_years = [str(x) for x in range(2010, 2011, 1)]
    list_years = years.split(',')
    #print(list_years)
    #list_months = ['01']
    list_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    for year in list_years:
        for m in list_months:
            print('month', m, 'year', year)
            research_query(month=m, year=year)

    return True


# Front Loops
def user_loop(afunc):

    retorno = 's'
    while retorno == 's':
        try:
            retorno = afunc
        except:
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            print(errormsg)
            print(print_exception())
            retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')

    t.sleep(3)


def portload_loop():

    retorno = 's'
    while retorno == 's':
        try:
            retorno = ploads_query()
        except:
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            print(errormsg)
            print(print_exception())
            retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')
    t.sleep(3)


def portships_loop():

    retorno = 's'
    while retorno == 's':
        try:
            retorno = pship_query()
        except:
            errormsg = "Unexpected error:" + str(sys.exc_info()[0]) + ' / ' + str(sys.exc_info()[1]) + ' / ' + \
                       str(sys.exc_info()[2])
            print(errormsg)
            print(print_exception())
            retorno = 'n'

        if retorno == 's':
            print('\n Executando consultas novamente. (Aperte CTRL+C para sair.) \n')
        else:
            print('\n Consultas Finalizadas. Encerrando aplicação. \n')
            print(' ...')
    t.sleep(3)


# CLI components
def start_local(switch_mode):

    #switch_mode = str(input("\n Deseja buscar portos ou navios? (digite 'portos' ou 'navios' para continuar): ")).lower()

    # shortcut test code
    #switch_mode = 'navios'

    if switch_mode == 'navios':

        switch_ship = 0
        while switch_ship == 0:

            switch_ship = str(input('\n Insira o tipo de execução IMO, ARQUIVO, ESTUDO ou ANALISE: ')).lower()

            #switch_ship = 'arquivo'  # shortcut test mode

            if switch_ship == 'imo':
                user_loop(imo_query())

            elif switch_ship == 'capitania':
                user_loop(cap_query())

            elif switch_ship == 'arquivo':
                analysis_type = str(input("\n  Escolha petróleo(óleo), container(teu):")).lower()
                if analysis_type in ['óleo', 'oleo', 'oil', 'petroleo', 'petróleo']:
                    user_loop(imo_multilist_query(amode='oil'))
                    switch_ship = 0
                elif analysis_type in ['container', 'teu', 'conteiner', 'contêiner']:
                    user_loop(imo_multilist_query(amode='teu'))
                    switch_ship = 0

            elif switch_ship == 'estudo':
                # TODO: Check some data format of integers cols df
                years = str(input('Diga os anos que deseja consultar separados por vírgula (2010,2019): '))
                multi_research_query(years)
                switch_ship = 1

            elif switch_ship == 'analise':
                analysis_type = str(input("\n  Escolha petróleo(óleo), container(teu):")).lower()
                if analysis_type in ['óleo', 'oleo', 'oil', 'petroleo', 'petróleo']:
                    metrics.create_analysis_oil()
                    switch_ship = True
                elif analysis_type in ['container', 'teu', 'conteiner', 'contêiner']:
                    metrics.create_analysis_teu()
                    switch_ship = True
                else:
                    print("\n Entrada inválida. Digite petróleo(óleo), container(teu) ou 'SAIR' para fechar a tela.")
                    switch_ship = False

            elif switch_ship == 'sair':
                break

            else:
                print("\n Entrada inválida. Digite 'IMO' ou 'CAPITANIA' para iniciar ou 'SAIR' para fechar a tela.")
                switch_ship = 0

    elif switch_mode == 'portos':

        switch_port = 0
        while switch_port == 0:

            switch_port = str(input("\n Insira o tipo de busca (Digite 'cargas' ou 'navios'): ")).lower()

            if switch_port == 'cargas':
                portload_loop()
            elif switch_port == 'navios':
                portships_loop()
            elif switch_port == 'sair':
                break
            else:
                print("\n Entrada inválida. Digite 'Cargas' ou 'Navios' para iniciar ou 'SAIR' para fechar a tela.")
                switch_port = 0


def test_analysis():

    profile_generator.run_plots()