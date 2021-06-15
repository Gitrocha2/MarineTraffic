import sqlite3

'''
Create configurations for local database creation.
TODO: Replace it to a cloud database service to persist data.
'''


def start_database():

    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('./Main/database/data/atr_info.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE loadsinfo (
            IDCarga integer,
            IDAtracacao integer,
            Origem String(32767),
            Destino String(32767),
            CDMercadoria String(32767),
            "Tipo Operação da Carga" String(32767),
            "Carga Geral Acondicionamento" String(32767),
            ConteinerEstado String(32767),
            "Tipo Navegação" String(32767),
            FlagAutorizacao String(32767),
            FlagCabotagem String(32767),
            FlagCabotagemMovimentacao String(32767),
            FlagConteinerTamanho String(32767),
            FlagLongoCurso String(32767),
            FlagMCOperacaoCarga String(32767),
            FlagOffshore String(32767),
            FlagTransporteViaInterioir String(32767),
            "Percurso Transporte em vias Interiores" String(32767),
            "Percurso Transporte Interiores" String(32767),
            STNaturezaCarga String(32767),
            STSH2 String(32767),
            STSH4 String(32767),
            "Natureza da Carga" String(32767),
            Sentido String(32767),
            TEU numeric,
            QTCarga numeric,
            VLPesoCargaBruta numeric,
            CDMercadoriaConteinerizada String(32767),
            VLPesoCargaCont numeric)""")

    conn.close()

    return


start_database()
