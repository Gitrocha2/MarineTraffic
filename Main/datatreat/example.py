import pandas as pd
from pathlib import Path


basepath = Path('.') / 'Main' / 'database' / 'raw' / 'all_loads.csv'
df = pd.read_csv(basepath, sep=',')
nocont = df[df['Natureza da Carga'] != 'Carga Conteinerizada'][0:10]
cont = df[df['Natureza da Carga'] == 'Carga Conteinerizada'][0:10]

nocont.to_csv(Path('.') / 'Main' / 'database' / 'raw' / 'nocont.csv', sep=';', index=False)
cont.to_csv(Path('.') / 'Main' / 'database' / 'raw' / 'cont.csv', sep=';', index=False)
