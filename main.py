from Main import massops
#from Main.datatreat.datatreats import runtreat
#from Main.datatreat.datatreatloads import runtreatsloads


if __name__ == '__main__':

    massops.start_local(switch_mode='navios')
    #massops.test_analysis()

    #runtreat()
    #runtreatsloads()
    print('done')


'''

./Main/database/data/atr_info.db loadsinfo cargas

SELECT * FROM loadsinfo WHERE IDAtracacao IN ({loadid})


./Main/database/data/atr_info.db atrstats atracações

SELECT * FROM atrstats WHERE [Nº do IMO] IN ({imolist})

## testing
'''