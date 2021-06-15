import pandas as pd
from pathlib import Path
from Main import functions


basepath = Path('..') / 'database'
wellspath = basepath / 'raw' / 'wells'

files_list = functions.find_files(wellspath)
#df_all_wells = pd.DataFrame()
df_well_list = []

for file in files_list:

    print(file)

    dfaux = pd.read_csv(wellspath / file, sep=',', encoding='utf-8-sig').fillna(0)
    nameaux = str(file).split('-')
    ref_date = f"01/{nameaux[-2]}/{nameaux[-1].split('.')[0]}"
    print(ref_date)
    dfaux['Reference_Date'] = ref_date
    df_well_list.append(dfaux)

print('all wells prod has been read')

df_full = functions.df_concat_reducer(df_list=df_well_list)
print('saving dataframe full')
df_full.to_csv(wellspath / 'all_wells_prod.csv', sep=';', encoding='cp1252', index=False)
print('done')
