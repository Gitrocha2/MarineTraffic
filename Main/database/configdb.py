import sqlite3

'''
Create configurations for local database creation.
TODO: Replace it to a cloud database service to persist data.
'''


def start_database():

    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE atrstats (
                IDAtracacao integer,
                TEsperaAtracacao numeric,
                TEsperaInicioOp numeric,
                TOperacao numeric,
                TEsperaDesatracacao numeric,
                TAtracado numeric,
                TEstadia numeric,
                CDTUP String(32767),
                IDBerco String(32767),
                Berço String(32767),
                "Porto Atracação" String(32767),
                "Apelido Instalação Portuária" String(32767),
                "Complexo Portuário" String(32767),
                "Tipo da Autoridade Portuária" String(32767),
                "Data Atracação" String(32767),
                "Data Chegada" String(32767),
                "Data Desatracação" String(32767),
                "Data Início Operação" String(32767),
                "Data Término Operação" String(32767),
                Ano String(32767),
                Mes String(32767),
                "Tipo de Operação" String(32767),
                "Tipo de Navegação da Atracação" String(32767),
                "Nacionalidade do Armador" String(32767),
                FlagMCOperacaoAtracacao String(32767),
                Terminal String(32767),
                Município String(32767),
                UF String(32767),
                SGUF String(32767),
                "Região Geográfica" String(32767),
                "Nº da Capitania" String(32767),
                "Nº do IMO" numeric)""")

    except:
        print('Database already exists or error in DB creation.')

    conn.close()

    return
