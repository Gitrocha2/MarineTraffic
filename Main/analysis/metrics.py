#import functions
from pathlib import Path
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

pd.options.mode.chained_assignment = None  # default='warn'


def find_folders(xpath, amode):

    result = []
    listdir = os.listdir(xpath)
    print('ListDIR', listdir)

    '''
    for filename in listdir:  # loop through all the files and folders
        if os.path.isdir(
                os.path.join(os.path.abspath("."), filename)):  # check whether the current object is a folder or not
            result.append(filename)
    '''

    for filename in listdir:  # loop through all the files and folders
        if os.path.isdir(xpath / filename):  # check whether the current object is a folder or not
            if filename.split('_')[0] == amode:
                result.append(filename)

    result.sort()

    return result


# Create custom reports and analysis

def create_analysis_oil():
    basepath = Path('.')
    #folder_type = str(input('Escolha a pasta para analisar: (Research ou Fleets): ')).lower()
    folder_type = 'Fleets'
    report_path = basepath / 'Reports' / folder_type
    #folders_list = functions.find_folders(report_path)
    folders_list = find_folders(report_path, 'oil')
    print(folders_list)

    print('Analysis is running... \n\n')

    for group in folders_list:

        print(f'\n\n ---------------------------- Analyzing the group:        ___ {group} ___ '
              f'----------------------------')
        trip_path = report_path / group / 'viagens'
        loads_path = report_path / group / 'cargas'
        ports_path = basepath / 'Inputs'

        print(trip_path)

        trips_df = pd.read_csv(trip_path / 'Resultado.csv', sep=';', encoding='cp1252')
        #print('\n\ndescribe: \n', trips_df.describe())

        trips_df[['VLPesoCargaBruta_IN', 'VLPesoCargaBruta_OUT']] = trips_df[['VLPesoCargaBruta_IN', 'VLPesoCargaBruta_OUT']].fillna(0)
        trips_df['VLPesoCargaBruta'] = trips_df['VLPesoCargaBruta_IN'] + trips_df['VLPesoCargaBruta_OUT']
        trips_df['Prancha'] = trips_df['VLPesoCargaBruta'] / trips_df['TOperacao']

        trips_df = trips_df.astype({'Prancha': float})
        #trips_df_ok = trips_df[~trips_df['Prancha'].isin([np.nan, np.inf, -np.inf, 0])]
        #print('\n\ndescribe new nok: \n', trips_df.describe())

        #prancha_mean = trips_df_ok.describe()['Prancha']['mean']
        #okrecords = trips_df_ok.describe()['Prancha']['count']
        # TODO: Adjust missing values or non operational trips and times meaures!!!!!!!!!!!!!!!!!!!!!!!
        trips_df = trips_df.fillna(0)

        # Print graphics - FILAS
        trips_df['TFilas'] = trips_df['TEsperaAtracacao'] + trips_df['TEsperaInicioOp'] + trips_df['TEsperaDesatracacao']
        data_filas = trips_df['TFilas']
        std_filas = int(data_filas.std(axis=0, skipna=True))
        data_filas = [record for record in data_filas if record < 5*std_filas]
        data_size = len(data_filas)
        nbins = 30 if data_size > 30 else 20
        hist1 = plt.figure(3)
        plt.hist(data_filas, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Tempo de Fila (h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Filas-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - PRANCHA
        trips_df['Prancha'] = pd.to_numeric(trips_df['Prancha'].fillna(0), errors='coerce')

        trips_df['Prancha'].loc[(trips_df['Prancha'].isin([np.inf, -np.inf, np.nan, 0])) & (trips_df['VLPesoCargaBruta'] > 0)] = trips_df.loc[(~trips_df['Prancha'].isin([np.inf, -np.inf, np.nan, 0])) & (trips_df['VLPesoCargaBruta'] > 0)].describe()['Prancha']['mean']
        trips_df_prancha = trips_df.loc[trips_df['VLPesoCargaBruta'] > 0]

        data_prancha_old = trips_df_prancha['Prancha'].tolist()

        trips_df_prancha = trips_df_prancha.loc[(trips_df_prancha['Prancha'] < (3*trips_df_prancha['Prancha'].std(axis=0, skipna=True)))
                                            & (trips_df_prancha['Prancha'] > (0.1*trips_df_prancha['Prancha'].mean(axis=0, skipna=True)))]

        data_prancha = trips_df_prancha['Prancha'].tolist()

        diffs = [data for data in data_prancha_old if data not in data_prancha]
        data_size = len(data_prancha)
        nbins = 30 if data_size > 30 else 20
        data_prancha.sort()
        hist1 = plt.figure(1)
        plt.hist(data_prancha, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Prancha (ton/h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Prancha-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - OPERAÇÃO
        data_ops = trips_df['TOperacao']
        std_prancha = int(data_ops.std(axis=0, skipna=True))
        data_ops = [record for record in data_ops if record < 5*std_prancha]
        data_size = len(data_ops)
        nbins = 30 if data_size > 30 else 20
        hist2 = plt.figure(2)
        plt.hist(data_ops, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Tempo de Operação (h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Operação-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - ESTADIA
        data_est = trips_df['TEstadia']
        std_prancha = int(data_est.std(axis=0, skipna=True))
        data_est = [record for record in data_est if record < 5*std_prancha]
        data_size = len(data_est)
        nbins = 30 if data_size > 30 else 20
        hist1 = plt.figure(5)
        plt.hist(data_est, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Tempo de Estadia (h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Estadia-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - VIAGENS
        # TODO: Adjust values to hours -> bug: in days, Separate ships from files
        trips_df['Chegada'] = pd.to_datetime(trips_df['Chegada'], errors='coerce', format='%d/%m/%Y %H:%M:%S')
        trips_df = trips_df.astype({'TEstadia': 'float'})
        ships_groups = trips_df.groupby(['IMO'])
        print('keys', ships_groups.groups.keys())

        #List of accumulated data of each ship to create a table
        IMOList = []
        TEsperaAtracacao = []
        TEsperaInicioOp = []
        TOperacao = []
        TEsperaDesatracacao = []
        TAtracado = []
        TEstadia = []
        TFilas = []
        VLPesoCargaBruta_IN = []
        VLPesoCargaBruta_OUT = []
        VLPesoCargaBruta = []
        Total_atracts = []

        for name, ship_df in ships_groups:
            IMOList.append(int(name))
            print(name)
            #print(ship_df)
            ship_df = ship_df.sort_values(by=['Chegada'], ascending=True)
            ship_df['Trip_Time_aux'] = ship_df.Chegada.diff() / np.timedelta64(1, 'D')
            #ship_df['Trip_Time'] = (ship_df['Trip_Time_aux'] - (ship_df['TEstadia'].shift(1) / 24))
            ship_df['Trip_Time'] = 0
            ship_df['Trip_Time'].loc[(ship_df['Trip_Time_aux'] == 0)] = 0
            ship_df['Trip_Time'].loc[(ship_df['Trip_Time_aux'] != 0)] = (ship_df['Trip_Time_aux'] - (ship_df['TEstadia'].shift(1) / 24))
            ship_df['Trip_Time'] = ship_df['Trip_Time'].shift(-1)

            data_trip = ship_df['TEstadia']
            std_prancha = int(data_trip.std(axis=0, skipna=True))
            data_trip = [record for record in data_trip if record < 10 * std_prancha]
            data_size = len(data_trip)
            nbins = 30 if data_size > 30 else 20
            hist1 = plt.figure(4)
            plt.hist(data_trip, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
            plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
            plt.xlabel('Tempo de Viagem (h)', fontsize=18)
            plt.ylabel('Ocorrência (%)', fontsize=16)
            plt.savefig(trip_path / f'Viagem-Hist-{group}.pdf')
            #plt.show()
            ship_df.to_csv(trip_path / f'Resultado-{name}.csv', index=False, sep=';', encoding='cp1252')

            # Analyze load transfer and Ports movement
            loads_df = pd.read_csv(loads_path / 'Cargas.csv', sep=';', encoding='cp1252')
            loads_df = loads_df[['IDAtracacao', 'Destino', 'Origem', 'Tipo Operação da Carga', 'Natureza da Carga', 'Sentido']]

            ships_loads_df = pd.merge(ship_df, loads_df,
                                      left_on=['IDAtracacao'],
                                      right_on=['IDAtracacao'],
                                      how='left')

            ports_df = pd.read_csv(ports_path / 'portcodes.csv', sep=';', encoding='utf-8-sig')

            ships_loads_ports = pd.merge(ships_loads_df.copy(), ports_df.copy(),
                                         left_on=['Destino'],
                                         right_on=['Portcode'],
                                         how='left')

            ships_loads_ports = ships_loads_ports.rename(columns={'Portname': 'Porto-destino', 'Country': 'Pais-destino'})
            ships_loads_ports.drop(['Portcode'], axis=1, inplace=True)

            ships_loads_ports_new = pd.merge(ships_loads_ports.copy(), ports_df.copy(),
                                             left_on=['Origem'],
                                             right_on=['Portcode'],
                                             how='left')

            ships_loads_ports_new = ships_loads_ports_new.rename(columns={'Portname': 'Porto-origem', 'Country': 'Pais-origem'})
            ships_loads_ports_new.drop(['Portcode'], axis=1, inplace=True)

            #print(ship_df.columns.values)
            ships_metrics = ships_loads_df[['TEsperaAtracacao', 'TEsperaInicioOp', 'TOperacao', 'TEsperaDesatracacao',
                                            'TAtracado', 'TEstadia', 'TFilas', 'VLPesoCargaBruta_IN', 'VLPesoCargaBruta_OUT',
                                            'VLPesoCargaBruta', 'Prancha', 'Trip_Time']].describe()

            end = ships_loads_df['Chegada'].iat[-1]
            start = ships_loads_df['Chegada'].iat[0]
            total_time = round((end - start) / np.timedelta64(1, 'D'), 1)
            print(total_time, 'dias operando. De', start, 'até', end)

            atr_wait_time_n = ships_metrics['TEsperaAtracacao']['count']
            atr_wait_time_acc = ships_metrics['TEsperaAtracacao']['mean'] * atr_wait_time_n
            TEsperaAtracacao.append(atr_wait_time_acc)

            opr_wait_time_n = ships_metrics['TEsperaInicioOp']['count']
            opr_wait_time_acc = ships_metrics['TEsperaInicioOp']['mean'] * opr_wait_time_n
            TEsperaInicioOp.append(opr_wait_time_acc)

            opr_time_n = ships_metrics['TOperacao']['count']
            opr_time_acc = ships_metrics['TOperacao']['mean'] * opr_time_n
            TOperacao.append(opr_time_acc)

            datr_wait_time_n = ships_metrics['TEsperaDesatracacao']['count']
            datr_wait_time_acc = ships_metrics['TEsperaDesatracacao']['mean'] * datr_wait_time_n
            TEsperaDesatracacao.append(datr_wait_time_acc)

            atr_time_n = ships_metrics['TAtracado']['count']
            atr_time_acc = ships_metrics['TAtracado']['mean'] * atr_time_n
            TAtracado.append(atr_time_acc)

            atr_full_time_n = ships_metrics['TEstadia']['count']
            atr_full_time_acc = ships_metrics['TEstadia']['mean'] * atr_full_time_n
            TEstadia.append(atr_full_time_acc)

            all_wait_time_n = ships_metrics['TFilas']['count']
            all_wait_time_acc = ships_metrics['TFilas']['mean'] * all_wait_time_n
            TFilas.append(all_wait_time_acc)

            all_load_in_n = ships_metrics['VLPesoCargaBruta_IN']['count']
            all_load_in_acc = ships_metrics['VLPesoCargaBruta_IN']['mean'] * all_load_in_n
            VLPesoCargaBruta_IN.append(all_load_in_acc)

            all_load_out_n = ships_metrics['VLPesoCargaBruta_OUT']['count']
            all_load_out_acc = ships_metrics['VLPesoCargaBruta_OUT']['mean'] * all_load_out_n
            VLPesoCargaBruta_OUT.append(all_load_out_acc)

            all_load_mov_n = ships_metrics['VLPesoCargaBruta']['count']
            all_load_mov_acc = ships_metrics['VLPesoCargaBruta']['mean'] * all_load_mov_n
            VLPesoCargaBruta.append(all_load_mov_acc)

            Total_atracts.append(ships_loads_ports_new.shape[0])

            ships_metrics.to_csv(trip_path / f'Metrics-{name}.csv', sep=';', encoding='cp1252')

            ships_loads_ports_new.to_csv(trip_path / f'Resultado-Loads-{name}.csv', index=False, sep=';', encoding='cp1252')

            #Configura gráfico de tempos de filas ao longo do tempo
            ships_loads_ports_new = ships_loads_ports_new.set_index('Chegada')
            #fig, ax = plt.subplots()
            #ax.plot(ships_loads_ports_new['VLPesoCargaBruta'] / 1000, color='black', label='Consumption')

            #ships_loads_ports_new[['TEsperaAtracacao',
            #                       'TEsperaInicioOp',
            #                       'TOperacao',
            #                       'TEsperaDesatracacao']].plot.area(ax=ax, linewidth=0)

            #ships_loads_ports_new[['TEsperaAtracacao',
            #                       'TEsperaInicioOp',
            #                       'TOperacao',
            #                       'TEsperaDesatracacao']].plot.bar(stacked=True)

            resampled = ships_loads_ports_new[['TEsperaAtracacao', 'TEsperaInicioOp', 'TOperacao', 'TEsperaDesatracacao']]\
                .resample('M').mean()

            ax = resampled.plot.bar(stacked=True)

            x_labels = resampled.index.strftime('%Y-%m')
            ax.set_xticklabels(x_labels)

            ##months = mdates.MonthLocator()
            #years_fmt = mdates.DateFormatter('%Y-%m')
            ##ax.xaxis.set_minor_locator(months)
            ##ax.xaxis.set_major_locator(mdates.YearLocator())
            #ax.xaxis.set_major_locator(mtick.MultipleLocator(60))
            #ax.xaxis.set_major_formatter(years_fmt)
            #ax.legend()
            #ax.set_ylabel('Tempo (horas)')
            plt.xticks(rotation=90)
            #fig.subplots_adjust(bottom=0.3)
            plt.show()
            plt.savefig(trip_path / f'Tempos-timeseries-{name}.pdf')

        fleet_metrics_acc = pd.DataFrame({'IMO': IMOList,
                                          'TEsperaAtracacao': TEsperaAtracacao,
                                          'TEsperaInicioOp': TEsperaInicioOp,
                                          'TOperacao': TOperacao,
                                          'TEsperaDesatracacao': TEsperaDesatracacao,
                                          'TAtracado': TAtracado,
                                          'TEstadia': TEstadia,
                                          'TFilas': TFilas,
                                          'VLPesoCargaBruta_IN': VLPesoCargaBruta_IN,
                                          'VLPesoCargaBruta_OUT': VLPesoCargaBruta_OUT,
                                          'VLPesoCargaBruta': VLPesoCargaBruta,
                                          'Total_Atr': Total_atracts})

        fleet_metrics_acc.to_csv(trip_path / 'Fleet-aggregated-Metrics.csv', index=False, sep=';', encoding='cp1252')
        #trips_df.to_csv(trip_path / 'Resultado-V5.csv', index=False, sep=';', encoding='cp1252')

    return print('\n\nDone processing data analysis service.')


def create_analysis_teu():
    basepath = Path('.')
    folder_type = 'Fleets'
    report_path = basepath / 'Reports' / folder_type
    folders_list = find_folders(report_path, 'teu')
    print('Group of analysis running for:', folders_list)

    for group in folders_list:

        print(f'\n\n ---------------------------- Analyzing the group:        ___ {group} ___ '
              f'----------------------------')
        trip_path = report_path / group / 'viagens'
        loads_path = report_path / group / 'cargas'
        ports_path = basepath / 'Inputs'

        print(trip_path)

        trips_df = pd.read_csv(trip_path / 'Resultado.csv', sep=';', encoding='cp1252')
        #print('\n\ndescribe: \n', trips_df.describe())

        trips_df[['TEUs_IN', 'TEUs_OUT']] = trips_df[['TEUs_IN', 'TEUs_OUT']].fillna(0)
        trips_df['TEU'] = trips_df['TEUs_IN'] + trips_df['TEUs_OUT']
        trips_df['Prancha'] = trips_df['TEU'] / trips_df['TOperacao']

        trips_df = trips_df.astype({'Prancha': float})
        #trips_df_ok = trips_df[~trips_df['Prancha'].isin([np.nan, np.inf, -np.inf, 0])]
        #print('\n\ndescribe new nok: \n', trips_df.describe())

        #prancha_mean = trips_df_ok.describe()['Prancha']['mean']
        #okrecords = trips_df_ok.describe()['Prancha']['count']
        # TODO: Adjust missing values or non operational trips and times meaures!!!!!!!!!!!!!!!!!!!!!!!
        trips_df = trips_df.fillna(0)

        # Print graphics - FILAS
        trips_df['TFilas'] = trips_df['TEsperaAtracacao'] + trips_df['TEsperaInicioOp'] + trips_df['TEsperaDesatracacao']
        data_filas = trips_df['TFilas']
        std_filas = int(data_filas.std(axis=0, skipna=True))
        data_filas = [record for record in data_filas if record < 5*std_filas]
        data_size = len(data_filas)
        nbins = 30 if data_size > 30 else 20
        hist1 = plt.figure(3)
        plt.hist(data_filas, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Tempo de Fila (h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Filas-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - PRANCHA
        trips_df['Prancha'] = pd.to_numeric(trips_df['Prancha'].fillna(0), errors='coerce')

        trips_df['Prancha'].loc[(trips_df['Prancha'].isin([np.inf, -np.inf, np.nan, 0]))
                              & (trips_df['TEU'] > 0)] = trips_df.loc[(~trips_df['Prancha'].isin([np.inf, -np.inf, np.nan, 0]))
                                                                    & (trips_df['TEU'] > 0)].describe()['Prancha']['mean']
        trips_df_prancha = trips_df.loc[trips_df['TEU'] > 0]

        data_prancha_old = trips_df_prancha['Prancha'].tolist()

        trips_df_prancha = trips_df_prancha.loc[(trips_df_prancha['Prancha'] < (3*trips_df_prancha['Prancha'].std(axis=0, skipna=True)))
                                            & (trips_df_prancha['Prancha'] > (0.1*trips_df_prancha['Prancha'].mean(axis=0, skipna=True)))]

        data_prancha = trips_df_prancha['Prancha'].tolist()

        diffs = [data for data in data_prancha_old if data not in data_prancha]
        data_size = len(data_prancha)
        nbins = 30 if data_size > 30 else 20
        data_prancha.sort()
        hist1 = plt.figure(1)
        plt.hist(data_prancha, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Prancha (TEUs/h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Prancha-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - OPERAÇÃO
        data_ops = trips_df['TOperacao']
        std_prancha = int(data_ops.std(axis=0, skipna=True))
        data_ops = [record for record in data_ops if record < 5*std_prancha]
        data_size = len(data_ops)
        nbins = 30 if data_size > 30 else 20
        hist2 = plt.figure(2)
        plt.hist(data_ops, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Tempo de Operação (h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Operação-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - ESTADIA
        data_est = trips_df['TEstadia']
        std_prancha = int(data_est.std(axis=0, skipna=True))
        data_est = [record for record in data_est if record < 5*std_prancha]
        data_size = len(data_est)
        nbins = 30 if data_size > 30 else 20
        hist1 = plt.figure(5)
        plt.hist(data_est, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
        plt.xlabel('Tempo de Estadia (h)', fontsize=18)
        plt.ylabel('Ocorrência (%)', fontsize=16)
        plt.savefig(trip_path / f'Estadia-Hist-{group}.pdf')
        #plt.show()

        # Print graphics - VIAGENS
        # TODO: Adjust values to hours -> bug: in days, Separate ships from files
        trips_df['Chegada'] = pd.to_datetime(trips_df['Chegada'], errors='coerce', format='%d/%m/%Y %H:%M:%S')
        trips_df = trips_df.astype({'TEstadia': 'float'})
        ships_groups = trips_df.groupby(['IMO'])
        print('keys', ships_groups.groups.keys())

        #List of accumulated data of each ship to create a table
        IMOList = []
        TEsperaAtracacao = []
        TEsperaInicioOp = []
        TOperacao = []
        TEsperaDesatracacao = []
        TAtracado = []
        TEstadia = []
        TFilas = []
        VLPesoCargaBruta_IN = []
        VLPesoCargaBruta_OUT = []
        VLPesoCargaBruta = []
        Total_atracts = []

        for name, ship_df in ships_groups:
            IMOList.append(int(name))
            print(name)
            #print(ship_df)
            ship_df = ship_df.sort_values(by=['Chegada'], ascending=True)
            ship_df['Trip_Time_aux'] = ship_df.Chegada.diff() / np.timedelta64(1, 'D')
            #ship_df['Trip_Time'] = (ship_df['Trip_Time_aux'] - (ship_df['TEstadia'].shift(1) / 24))
            ship_df['Trip_Time'] = 0
            ship_df['Trip_Time'].loc[(ship_df['Trip_Time_aux'] == 0)] = 0
            ship_df['Trip_Time'].loc[(ship_df['Trip_Time_aux'] != 0)] = (ship_df['Trip_Time_aux'] - (ship_df['TEstadia'].shift(1) / 24))
            ship_df['Trip_Time'] = ship_df['Trip_Time'].shift(-1)

            data_trip = ship_df['TEstadia']
            std_prancha = int(data_trip.std(axis=0, skipna=True))
            data_trip = [record for record in data_trip if record < 10 * std_prancha]
            data_size = len(data_trip)
            nbins = 30 if data_size > 30 else 20
            hist1 = plt.figure(4)
            plt.hist(data_trip, weights=(np.ones(data_size) / data_size), bins=nbins, histtype="step")
            plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
            plt.xlabel('Tempo de Viagem (h)', fontsize=18)
            plt.ylabel('Ocorrência (%)', fontsize=16)
            plt.savefig(trip_path / f'Viagem-Hist-{group}.pdf')
            #plt.show()
            ship_df.to_csv(trip_path / f'Resultado-{name}.csv', index=False, sep=';', encoding='cp1252')

            # Analyze load transfer and Ports movement
            loads_df = pd.read_csv(loads_path / 'Cargas.csv', sep=';', encoding='cp1252')
            loads_df = loads_df[['IDAtracacao', 'Destino', 'Origem', 'Tipo Operação da Carga', 'Natureza da Carga', 'Sentido']]

            ships_loads_df = pd.merge(ship_df, loads_df,
                                      left_on=['IDAtracacao'],
                                      right_on=['IDAtracacao'],
                                      how='left')

            ports_df = pd.read_csv(ports_path / 'portcodes.csv', sep=';', encoding='utf-8-sig')

            ships_loads_ports = pd.merge(ships_loads_df.copy(), ports_df.copy(),
                                         left_on=['Destino'],
                                         right_on=['Portcode'],
                                         how='left')

            ships_loads_ports = ships_loads_ports.rename(columns={'Portname': 'Porto-destino', 'Country': 'Pais-destino'})
            ships_loads_ports.drop(['Portcode'], axis=1, inplace=True)

            ships_loads_ports_new = pd.merge(ships_loads_ports.copy(), ports_df.copy(),
                                             left_on=['Origem'],
                                             right_on=['Portcode'],
                                             how='left')

            ships_loads_ports_new = ships_loads_ports_new.rename(columns={'Portname': 'Porto-origem', 'Country': 'Pais-origem'})
            ships_loads_ports_new.drop(['Portcode'], axis=1, inplace=True)

            #print(ship_df.columns.values)
            ships_metrics = ships_loads_df[['TEsperaAtracacao', 'TEsperaInicioOp', 'TOperacao', 'TEsperaDesatracacao',
                                            'TAtracado', 'TEstadia', 'TFilas', 'TEU', 'TEUs_IN', 'TEUs_OUT',
                                            'Prancha', 'Trip_Time']].describe()

            end = ships_loads_df['Chegada'].iat[-1]
            start = ships_loads_df['Chegada'].iat[0]
            total_time = round((end - start) / np.timedelta64(1, 'D'), 1)
            print(total_time, 'dias operando. De', start, 'até', end)

            atr_wait_time_n = ships_metrics['TEsperaAtracacao']['count']
            atr_wait_time_acc = ships_metrics['TEsperaAtracacao']['mean'] * atr_wait_time_n
            TEsperaAtracacao.append(atr_wait_time_acc)

            opr_wait_time_n = ships_metrics['TEsperaInicioOp']['count']
            opr_wait_time_acc = ships_metrics['TEsperaInicioOp']['mean'] * opr_wait_time_n
            TEsperaInicioOp.append(opr_wait_time_acc)

            opr_time_n = ships_metrics['TOperacao']['count']
            opr_time_acc = ships_metrics['TOperacao']['mean'] * opr_time_n
            TOperacao.append(opr_time_acc)

            datr_wait_time_n = ships_metrics['TEsperaDesatracacao']['count']
            datr_wait_time_acc = ships_metrics['TEsperaDesatracacao']['mean'] * datr_wait_time_n
            TEsperaDesatracacao.append(datr_wait_time_acc)

            atr_time_n = ships_metrics['TAtracado']['count']
            atr_time_acc = ships_metrics['TAtracado']['mean'] * atr_time_n
            TAtracado.append(atr_time_acc)

            atr_full_time_n = ships_metrics['TEstadia']['count']
            atr_full_time_acc = ships_metrics['TEstadia']['mean'] * atr_full_time_n
            TEstadia.append(atr_full_time_acc)

            all_wait_time_n = ships_metrics['TFilas']['count']
            all_wait_time_acc = ships_metrics['TFilas']['mean'] * all_wait_time_n
            TFilas.append(all_wait_time_acc)

            all_load_in_n = ships_metrics['TEUs_IN']['count']
            all_load_in_acc = ships_metrics['TEUs_IN']['mean'] * all_load_in_n
            VLPesoCargaBruta_IN.append(all_load_in_acc)

            all_load_out_n = ships_metrics['TEUs_OUT']['count']
            all_load_out_acc = ships_metrics['TEUs_OUT']['mean'] * all_load_out_n
            VLPesoCargaBruta_OUT.append(all_load_out_acc)

            all_load_mov_n = ships_metrics['TEU']['count']
            all_load_mov_acc = ships_metrics['TEU']['mean'] * all_load_mov_n
            VLPesoCargaBruta.append(all_load_mov_acc)

            Total_atracts.append(ships_loads_ports_new.shape[0])

            ships_metrics.to_csv(trip_path / f'Metrics-{name}.csv', sep=';', encoding='cp1252')

            ships_loads_ports_new.to_csv(trip_path / f'Resultado-Loads-{name}.csv', index=False, sep=';', encoding='cp1252')

            #Configura gráfico de tempos de filas ao longo do tempo
            ships_loads_ports_new = ships_loads_ports_new.set_index('Chegada')
            #fig, ax = plt.subplots()
            #ax.plot(ships_loads_ports_new['VLPesoCargaBruta'] / 1000, color='black', label='Consumption')

            #ships_loads_ports_new[['TEsperaAtracacao',
            #                       'TEsperaInicioOp',
            #                       'TOperacao',
            #                       'TEsperaDesatracacao']].plot.area(ax=ax, linewidth=0)

            #ships_loads_ports_new[['TEsperaAtracacao',
            #                       'TEsperaInicioOp',
            #                       'TOperacao',
            #                       'TEsperaDesatracacao']].plot.bar(stacked=True)

            resampled = ships_loads_ports_new[['TEsperaAtracacao', 'TEsperaInicioOp', 'TOperacao', 'TEsperaDesatracacao']]\
                .resample('M').mean()

            ax = resampled.plot.bar(stacked=True)

            x_labels = resampled.index.strftime('%Y-%m')
            ax.set_xticklabels(x_labels)

            ##months = mdates.MonthLocator()
            #years_fmt = mdates.DateFormatter('%Y-%m')
            ##ax.xaxis.set_minor_locator(months)
            ##ax.xaxis.set_major_locator(mdates.YearLocator())
            #ax.xaxis.set_major_locator(mtick.MultipleLocator(60))
            #ax.xaxis.set_major_formatter(years_fmt)
            #ax.legend()
            #ax.set_ylabel('Tempo (horas)')
            plt.xticks(rotation=90)
            #fig.subplots_adjust(bottom=0.3)
            plt.show()
            plt.savefig(trip_path / f'Tempos-timeseries-{name}.pdf')

        fleet_metrics_acc = pd.DataFrame({'IMO': IMOList,
                                          'TEsperaAtracacao': TEsperaAtracacao,
                                          'TEsperaInicioOp': TEsperaInicioOp,
                                          'TOperacao': TOperacao,
                                          'TEsperaDesatracacao': TEsperaDesatracacao,
                                          'TAtracado': TAtracado,
                                          'TEstadia': TEstadia,
                                          'TFilas': TFilas,
                                          'TEUs_IN': VLPesoCargaBruta_IN,
                                          'TEUs_OUT': VLPesoCargaBruta_OUT,
                                          'TEU': VLPesoCargaBruta,
                                          'Total_Atr': Total_atracts})

        fleet_metrics_acc.to_csv(trip_path / 'Fleet-aggregated-Metrics.csv', index=False, sep=';', encoding='cp1252')
        #trips_df.to_csv(trip_path / 'Resultado-V5.csv', index=False, sep=';', encoding='cp1252')

    return print('\n\nDone processing data analysis service.')

