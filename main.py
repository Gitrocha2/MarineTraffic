from Main import massops


if __name__ == '__main__':

    massops.start_local(switch_mode='navios')

    print('done')



'''

./Main/database/data/atr_info.db atr_info cargas

SELECT * FROM loadsinfo WHERE IDAtracacao IN ({loadid})


./Main/database/data/atr_info.db atrstats atracações

SELECT * FROM atrstats WHERE [Nº do IMO] IN ({imolist})

'''