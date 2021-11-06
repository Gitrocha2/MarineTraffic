# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta
import random
from scipy.stats import uniform, norm, truncnorm
import time
from pathlib import Path
from IPython.display import display, HTML


def model_func(t_vec, qi, di, b, p_months):

    if b == 0:
        q_vec = qi*np.exp(-di*t_vec)
    elif b == 1:
        q_vec = qi/(1 + di*t_vec)
    else:
        q_vec = qi/(1+b*di*t_vec)**(1/b)
    
    q_vec = np.pad(q_vec, (p_months, 0), 'constant', constant_values=(qi, 0))[:len(t_vec)]

    
    return q_vec


def accum_func(q_vec, elapsed_days):
    #CHECK FORMULA
    roll_sum_vec = np.cumsum(elapsed_days*q_vec[:-1])
    roll_sum_vec = np.append(roll_sum_vec, roll_sum_vec + 30.*q_vec[:-1])

    return roll_sum_vec

########################################
# Field Forecast
########################################
def field_forecast(date_init, op_sched, q_min, rem_reserves, eor_ind, date_eor):
    
    t_0       = 0
    t_end     = 1000
    t_num     = t_end + 1
    t_vec     = np.linspace(t_0, t_end, t_num) # Months

    date_vec  = [date_init + relativedelta(months = i) for i in t_vec]
    elapsed_days  = []
    
    for i in range(len(date_vec)-1):
        elapsed_days.append((date_vec[i+1]-date_vec[i]).days)
    
    num_wells = len(op_sched)
    
    df_rates  = pd.DataFrame() 
    df_acumm  = pd.DataFrame()  
    
    params_mat= np.zeros((4, num_wells))
    
    for i in range(num_wells):
        date_well = datetime(op_sched[i,1], op_sched[i,0], 1)
        index     = date_vec.index(date_well)
        
        # First Well Model Params
        q_init    = 30
        d_init    = 0.05
        b_init    = 1
        plat_init = 24
        
        # First Modelled Well - Base Point Parameters
        if i == 0:
            q_vec = model_func(t_vec, q_init, d_init, b_init, plat_init)
                        
        # Efficiency Decrease Due to Depletion - Time Dependence
        else:
            eff_factor  = 1 - (df_acumm.sum(axis=1)[index]/1000/rem_reserves)
            q_init = q_init*eff_factor
            
            q_vec  = model_func(t_vec, q_init, d_init, b_init, plat_init)
      
        #CHAECK THIS!! 
        if eor_ind == 1:
            index_eor = date_vec.index(date_eor)
            pos_ind   = index_eor-index
            
            #[Normal, Pre EOr, Post EOR] vs time 
            
            if pos_ind > 0:
                q_init    = q_vec[pos_ind]*1.4
                d_init    = 0.02
                b_init    = 0.18
                plat_init = 36
                
                q_vec_eor = model_func(t_vec, q_init, d_init, b_init, plat_init)
                q_vec[pos_ind:]  = q_vec_eor[0:len(q_vec[pos_ind:])]
            
            # New Well Post-EOR
            else:
                q_init    = q_vec[0]*1.4
                d_init    = 0.02
                b_init    = 0.18
                plat_init = 48
                
                q_vec  = model_func(t_vec, q_init, d_init, b_init, plat_init)

        params_mat[:,i] = [q_init, d_init, b_init, plat_init]
        
        if index != 0:
            q_vec     = np.pad(q_vec, (index, 0), 'constant')[0:t_end+1]
        
        min_prod_vals = np.flatnonzero(q_vec > q_min)
    
        if min_prod_vals.size != 0:
            q_vec[min_prod_vals[-1]:] = 0
        else:
            q_vec = q_vec*0
            
        df_rates[i]   = q_vec
        df_acumm[i]   = accum_func(q_vec, elapsed_days)
    
    df_rates.index = date_vec
    df_acumm.index = date_vec
    
    return df_rates, df_acumm, params_mat


########################################
# Field Forecast
########################################
def count_wells(df_rates):
    df_new_wells = pd.DataFrame()
    df_new_wells['Dates'] = df_rates.ne(0).idxmax()
    df_new_wells['Num']   = 1
    df_new_wells = df_new_wells.groupby('Dates').sum()

    df_wells     = df_rates.astype(bool).astype(int)

    return df_new_wells, df_wells


def operating_sched(year_init, num_wells):

    #basepath = Path('.')
    #report_path = basepath / 'Reports' / 'Fleets'

    #group = 'teu_Fleet-Login'
    #trip_path = report_path / group / 'viagens'

    #file_path = trip_path / 'Resultado-9327669.csv'

    #op_sched  = pd.read_csv(file_path, encoding='cp1252', sep=';')
    #op_sched  = op_sched.to_numpy()

    op_sched  = pd.DataFrame()
#     year_init = 1980
    ctr = 1

    month_list = []
    yr_list    = [] 
    for i in range(num_wells):
        month_list.append(random.randint(1, 12))
        yr_list.append(year_init)
        ctr += 1

        if year_init<2000:
            test = 8
        elif year_init>2010:
            test = 12
        else:
            test = 25

        if ctr>test:
            ctr = 1
            year_init += 1

    op_sched['Month'] = month_list
    op_sched['Year']  = yr_list
    op_sched.sort_values(by=['Month', 'Year'])

    op_sched  = op_sched.to_numpy()
    
    return op_sched


def run_plots():

    #######################################
    # Observed Data
    ########################################

    basepath = Path('.')
    report_path = basepath / 'Reports' / 'Fleets'

    group = 'teu_Fleet-Login'
    trip_path = report_path / group / 'viagens'

    file_path = trip_path / 'Resultado-9327669.csv'

    print(file_path)


    obs_data = pd.read_csv(file_path, encoding='cp1252', sep=';')

    obs_data['Chegada'] = pd.to_datetime(obs_data['Chegada'])

    obs_data.info()

    date_vec = obs_data.Chegada

    elapsed_days      = []
    for i in range(len(date_vec)-1):
        elapsed_days.append((date_vec[i+1]-date_vec[i]).days)

    #obs_data['Acumm'] = accum_func(obs_data['TEstadia'], elapsed_days)

    df_obs_acumm = accum_func(obs_data['TEstadia'], elapsed_days)

    ########################################
    # Input
    ########################################
    date_init = datetime(1979, 6, 1)
    date_eor  = datetime(2000, 1, 1)
    op_sched  = operating_sched(1980, 230)

    ########################################
    # Models
    ########################################

    # rem_reserves in millions of barrels
    # Everything else in thousands of barrels
    # EOR time dependence of wells - Efficiency factor

    print('models')
    #df_rates, df_acumm, params_mat             = field_forecast(date_init, op_sched, 0.5, 9298.25, 0, 0)

    print('next')

    #df_rates_sec, df_acumm_sec, params_mat_sec = field_forecast(date_init, op_sched, 0.5, 9298.25*1.1, 1, date_eor)

    ########################################
    # Figures
    ########################################

    fig, ax = plt.subplots(figsize = [10,5])

    ax.plot(obs_data['TEstadia'], 'bx', linewidth = 2.5)
#    ax.plot(obs_data['TOperacao'], 'k', linewidth=2.5)
    #ax.plot(df_rates.sum(axis=1), 'k', linewidth = 2.5)
    #ax.plot(df_rates_sec.sum(axis=1), 'r--', linewidth = 2.5)
    ax.set_title('Liquid Production', fontweight = 'bold')
    ax.set_ylabel('Rate, 000 b/d', fontweight = 'bold')
    ax.set_xlabel('Date', fontweight = 'bold')

    axb = ax.twinx()
    axb.plot(obs_data['TOperacao'], 'k', linewidth=2.5)
    axb.set_ylabel('Cummulative, 000 bls', fontweight = 'bold')
    ax.legend(['Observed', 'Primary Model'], loc = 'center right')

    print('show 2nd')

    plt.tight_layout()
    plt.show()

'''
    axb = ax.twinx()
    axb.plot(obs_data['Acumm'], 'bx', linewidth = 2.5)
    axb.plot(df_acumm.sum(axis=1), 'k', linewidth = 2.5)
    axb.plot(df_acumm_sec.sum(axis=1), 'r--', linewidth = 2.5)
    axb.set_ylabel('Cummulative, 000 bls', fontweight = 'bold')

    ax.legend(['Observed', 'Primary Model', 'Secondary Model'], loc = 'center right')

    plt.tight_layout()
    plt.show()

    ########################################
    # Single Well
    ########################################

    # fig, ax  = plt.subplots(figsize = [10,5])
    # ax.plot(df_rates[1], 'k', linewidth = 2.5)
    # ax.plot(df_rates_sec[1], 'r--', linewidth = 2.5)
    # ax.set_title('Liquid Production', fontweight = 'bold')
    # ax.set_ylabel('Rate, 000 b/d', fontweight = 'bold')
    # ax.set_xlabel('Date', fontweight = 'bold')
    # plt.tight_layout()
    # plt.show()

    ########################################
    # Recovery Factor
    ########################################
    # field_OOIP = 32822.56

    # fig, ax  = plt.subplots(figsize = [10,5])
    # ax.plot(obs_data['Acumm']/field_OOIP/1000, 'bx', linewidth = 2.5)
    # ax.plot(df_acumm.sum(axis=1)/field_OOIP/1000, 'k', linewidth = 2.5)
    # ax.plot(df_acumm_sec.sum(axis=1)/field_OOIP/1000, 'r--', linewidth = 2.5)
    # ax.set_title('Recovery Factor', fontweight = 'bold')
    # ax.set_ylabel('Recovery Factor', fontweight = 'bold')
    # ax.legend(['Observed', 'Primary', 'Secondary'], loc = 'center right')
    # plt.tight_layout()
    # plt.show()

    # GOR
    # Stats
    # Elapsed times
    ########################################
    # New Wells and Operating Wells
    ########################################

    df_new_wells, df_wells =  count_wells(df_rates)
    df_new_wells_sec, df_wells_sec =  count_wells(df_rates_sec)

    fig, ax  = plt.subplots(figsize = [10,5])
    ax.plot(df_new_wells, 'kx', linewidth = 2.5)
    ax.plot(df_new_wells_sec, 'rx', linewidth = 2.5)
    ax.set_ylabel('Number of New Wells', fontweight = 'bold')
    ax.set_xlabel('Date', fontweight = 'bold')

    axb = ax.twinx()
    axb.plot(df_wells.sum(axis=1), 'k', linewidth = 2.5)
    axb.plot(df_wells_sec.sum(axis=1), 'r--', linewidth = 2.5)
    axb.set_ylabel('Number of Operating Wells', fontweight = 'bold')
    axb.set_xlabel('Date', fontweight = 'bold')

    ax.legend(['Primary', 'Secondary'], loc = 'center right')
    plt.tight_layout()
    plt.show()

    ########################################
    # Recovery Factor
    ########################################
    field_OOIP = 32822.56

    fig, ax  = plt.subplots(figsize = [10,5])
    ax.plot(obs_data['Acumm']/field_OOIP/1000, 'bx', linewidth = 2.5)
    ax.plot(df_acumm.sum(axis=1)/field_OOIP/1000, 'k', linewidth = 2.5)
    ax.plot(df_acumm_sec.sum(axis=1)/field_OOIP/1000, 'r--', linewidth = 2.5)
    ax.set_title('Recovery Factor', fontweight = 'bold')
    ax.set_ylabel('Recovery Factor', fontweight = 'bold')
    ax.legend(['Observed', 'Primary', 'Secondary'], loc = 'center right')
    plt.tight_layout()
    plt.show()

    ########################################
    # Reserve Recovery Factor
    ########################################
    field_Oreserves_orig = 9298.25

    fig, ax  = plt.subplots(figsize = [10,5])
    ax.plot(obs_data['Acumm']/field_Oreserves_orig*1.1/1000, 'bx', linewidth = 2.5)
    ax.plot(df_acumm.sum(axis=1)/field_Oreserves_orig/1000, 'k', linewidth = 2.5)
    ax.plot(df_acumm_sec.sum(axis=1)/field_Oreserves_orig*1.1/1000, 'r--', linewidth = 2.5)
    ax.set_title('Reserve Recovery Efficiency', fontweight = 'bold')
    ax.set_ylabel('Recovery Factor', fontweight = 'bold')
    ax.legend(['Observed', 'Primary', 'Secondary'], loc = 'center right')
    plt.tight_layout()
    plt.show()

    ########################################
    # Well Stats
    ########################################

    acumm_stats = df_acumm.describe()
    rates_stats = df_rates.describe()

    acumm_stats_sec = df_acumm_sec.describe()
    rates_stats_sec = df_rates_sec.describe()

    # Average Liquid Rate
    fig, ax  = plt.subplots(figsize = [10,5])
    ax       = sns.distplot(rates_stats.loc['mean'], kde = False, bins = 20)
    ax       = sns.distplot(rates_stats_sec.loc['mean'], kde = False, bins = 20)
    ax.set_title('Average Liquid Rate [000 b/d]', fontweight = 'bold')
    ax.set_xlabel('Liquids, 000 b/d', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')
    ax.legend(['Primary', 'Secondary'], loc = 'best')
    plt.show()

    # Average Acummulated
    fig, ax  = plt.subplots(figsize = [10,5])
    ax       = sns.distplot(acumm_stats.loc['mean'], kde = False, bins = 20)
    ax       = sns.distplot(acumm_stats_sec.loc['mean'], kde = False, bins = 20)
    ax.set_title('Average Acummulated [000 bls]', fontweight = 'bold')
    ax.set_xlabel('Liquids, 000 bls', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')
    ax.legend(['Primary', 'Secondary'], loc = 'best')
    plt.show()

    # Average Well Life - BY TIME
    fig, ax  = plt.subplots(figsize = [10,5])
    ax       = sns.distplot(df_rates.astype(bool).sum(axis=0)/12, kde = False, bins = 20)
    ax       = sns.distplot(df_rates_sec.astype(bool).sum(axis=0)/12, kde = False, bins = 20)
    ax.set_title('Average Well Life', fontweight = 'bold')
    ax.set_xlabel('Well Life [Yrs]', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')
    ax.legend(['Primary', 'Secondary'], loc = 'best')
    plt.show()

    # Initial Rate
    fig, ax  = plt.subplots(figsize = [10,5])
    ax       = sns.distplot(params_mat[0,:], kde = False, bins = 20)
    ax       = sns.distplot(params_mat_sec[0,:], kde = False, bins = 20)
    ax.set_title('Average Well Life', fontweight = 'bold')
    ax.set_xlabel('Well Life [Yrs]', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')
    ax.legend(['Primary', 'Secondary'], loc = 'best')
    plt.show()

    ######################################################################################
    # Probabilistic Distributions - FROM DATA?
    ######################################################################################
    n_trials    = 50
    seed        = 0

    my_mean     = 9298.25*1.1
    my_std      = 9298.25*1.1*0.2
    a, b        = (0 - my_mean) / my_std, (100000 - my_mean) / my_std
    reserves_dist = truncnorm.rvs(a, b, loc = my_mean, scale = my_std, size = n_trials, random_state = seed)

    fig, ax     = plt.subplots(figsize = [10,5])
    ax          = sns.distplot(reserves_dist, kde = False)
    ax.set_title('Probability Distribution', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')
    ax.set_xlabel('IP-Rate', fontweight = 'bold')
    plt.show()

    ########################################
    # Observed Data
    ########################################
    # obs_data  = pd.read_csv(file_path, index_col=9)
    # date_vec  = obs_data.index

    elapsed_days      = []
    for i in range(len(date_vec)-1):
        elapsed_days.append((date_vec[i+1]-date_vec[i]).days)

    obs_data['Acumm'] = accum_func(obs_data['TEstadia'], elapsed_days)

    ########################################
    # Input
    ########################################
    date_init = datetime(1979, 6, 1)
    date_eor  = datetime(2000, 1, 1)

    op_sched_sens = [operating_sched(1980, 350), operating_sched(1980, 230), operating_sched(1980, 150)]

    ######################################################################################
    # Monte Carlo
    ######################################################################################

    iter_opsched = 1
    op_sched_sens_rates = []
    op_sched_sens_acumm = []


    for op_sched_iter in op_sched_sens:

        print('--------------------------------------------------------------')
        print('Operating Schedule ' + str(iter_opsched))
        print('--------------------------------------------------------------')

        elapsed_tot    = 0

        df_montecarlo_rates = []
        df_montecarlo_acumm = []

        for i in range(n_trials):

            t = time.time()

            df_rates_MC, df_acumm_MC, params_mat = field_forecast(date_init, op_sched_iter, 0.5, reserves_dist[i], 1, date_eor)

            df_montecarlo_rates.append(df_rates_MC)
            df_montecarlo_acumm.append(df_acumm_MC)



            elapsed      = time.time() - t
            elapsed_tot += elapsed
            print('-------------------------------')
            print('Realization ' + str(i+1))
            print('Iteration Time [min]    = ' + str(round(elapsed/60,2)))
            print('Total Time     [min]    = ' + str(round(elapsed_tot/60,2)))
            print('-------------------------------')

        op_sched_sens_rates.append(df_montecarlo_rates)
        op_sched_sens_acumm.append(df_montecarlo_acumm)
        iter_opsched += 1

    op_sched_sens_rates.append(df_montecarlo_rates)
    op_sched_sens_acumm.append(df_montecarlo_acumm)

    temp_list1 = []
    temp_list2 = []
    temp_list3 = []

    for op_sched_iter in range(3):
    # for op_sched_iter in [1]:
        df_sum_rates = pd.DataFrame()
        df_sum_acumm = pd.DataFrame()

        init_rates_list   = []
        avg_life_list     = []
        total_acumms_list = []

        df_montecarlo_rates = op_sched_sens_rates[op_sched_iter]
        df_montecarlo_acumm = op_sched_sens_acumm[op_sched_iter]

        for i in range(n_trials):
            real_sum_rate   = df_montecarlo_rates[i].sum(axis=1)
            df_sum_rates[i] = real_sum_rate

            res = [next((j for k, j in enumerate(df_montecarlo_rates[i][col]) if j != 0), (0)) for col in df_montecarlo_rates[i]]
            init_rates_list.extend(res)
            avg_life_list.append((df_montecarlo_rates[i].astype(bool).sum(axis=0)/12).values.tolist())
            # initial rates, total acums, average life

        for i in range(n_trials):
            real_sum_acumm = df_montecarlo_acumm[i].sum(axis=1)
            df_sum_acumm[i] = real_sum_acumm

            total_acumms_list.append(df_montecarlo_acumm[i].values[-1].tolist())

        temp_list1.append(avg_life_list)
        temp_list2.append(init_rates_list)
        temp_list3.append(total_acumms_list)

    ########################################
    # Figures
    ########################################
    # Oil Rate

    fig, ax  = plt.subplots(figsize = [10,5])
    ax.plot(df_sum_rates, 'k', linewidth = 1.5, alpha = 0.5)
    ax.plot(obs_data['TEstadia'], 'bx', linewidth = 2.5)

    perc_mat = np.transpose(df_sum_rates.to_numpy())
    p_10     = np.percentile(perc_mat, 10, axis = 0)
    p_50     = np.percentile(perc_mat, 50, axis = 0)
    p_90     = np.percentile(perc_mat, 90, axis = 0)
    ax.plot(df_sum_rates.index, p_10,  '--r', linewidth = 1.5)
    ax.plot(df_sum_rates.index, p_50,  '--r', linewidth = 1.5)
    ax.plot(df_sum_rates.index, p_90,  '--r', linewidth = 1.5)

    ax.set_title('Liquid Production', fontweight = 'bold')
    ax.set_ylabel('Rate, 000 b/d', fontweight = 'bold')
    ax.set_xlabel('Date', fontweight = 'bold')
    ax.legend(['Observed', 'Model'], loc = 'best')

    plt.tight_layout()
    plt.show()

    # Oil Acumm
    fig, ax  = plt.subplots(figsize = [10,5])

    ax.plot(df_sum_acumm, 'k', linewidth = 1.5,  alpha = 0.5)
    ax.plot(obs_data['Acumm'], 'bx', linewidth = 2.5)

    perc_mat = np.transpose(df_sum_acumm.to_numpy())
    p_10     = np.percentile(perc_mat, 10, axis = 0)
    p_50     = np.percentile(perc_mat, 50, axis = 0)
    p_90     = np.percentile(perc_mat, 90, axis = 0)
    ax.plot(df_sum_acumm.index, p_10,  '--r', linewidth = 1.5)
    ax.plot(df_sum_acumm.index, p_50,  '--r', linewidth = 1.5)
    ax.plot(df_sum_acumm.index, p_90,  '--r', linewidth = 1.5)

    ax.set_title('Liquid Acumm', fontweight = 'bold')
    ax.set_xlabel('Date', fontweight = 'bold')
    ax.set_ylabel('Cummulative, 000 bls', fontweight = 'bold')

    ax.legend(['Observed', 'Model'], loc = 'best')

    plt.tight_layout()
    plt.show()

    ## STATS PER WELL vs STATS PER REALIZATION

    # Well Life

    fig, ax  = plt.subplots(figsize = [10,5])
    # ax       = sns.distplot(avg_life_list, kde = False, bins = 20)

    ax       = sns.distplot(temp_list1[0], kde = False, bins = 20)
    ax       = sns.distplot(temp_list1[1], kde = False, bins = 20)
    ax       = sns.distplot(temp_list1[2], kde = False, bins = 20)
    ax.set_title('Average Well Life', fontweight = 'bold')
    ax.set_xlabel('Well Life [Yrs]', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')
    ax.legend(['350 Wells', '230 Wells', '150 Wells'], loc = 'best')

    plt.show()

    # Initial Rate

    fig, ax  = plt.subplots(figsize = [10,5])
    # ax       = sns.distplot(init_rates_list, kde = False, bins = 20)

    ax       = sns.distplot(temp_list2[0], kde = False, bins = 20)
    ax       = sns.distplot(temp_list2[1], kde = False, bins = 20)
    ax       = sns.distplot(temp_list2[2], kde = False, bins = 20)
    ax.set_title('Initial Liquid Rate', fontweight = 'bold')
    ax.set_xlabel('Liquid Rate, 000 b/d', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')

    ax.legend(['350 Wells', '230 Wells', '150 Wells'], loc = 'best')

    plt.show()

    # Total Acumm

    fig, ax  = plt.subplots(figsize = [10,5])
    # ax       = sns.distplot(total_acumms_list, kde = False, bins = 20)

    ax       = sns.distplot(temp_list3[0], kde = False, bins = 20)
    ax       = sns.distplot(temp_list3[1], kde = False, bins = 20)
    ax       = sns.distplot(temp_list3[2], kde = False, bins = 20)
    ax.set_title('Total Well Acummulation', fontweight = 'bold')
    ax.set_xlabel('Total Well Acummulation, 000 b', fontweight = 'bold')
    ax.set_ylabel('Count', fontweight = 'bold')

    ax.legend(['350 Wells', '230 Wells', '150 Wells'], loc = 'best')

    plt.show()

    t_0       = 0
    t_end     = 500
    t_num     = t_end + 1
    t_vec     = np.linspace(t_0, t_end, t_num) # Months

    date_init = datetime(2020, 1, 1)
    date_vec  = [date_init + relativedelta(months = i) for i in t_vec]

    elapsed_days  = []
    for i in range(len(date_vec)-1):
        elapsed_days.append((date_vec[i+1]-date_vec[i]).days)

    #Di per month
    q_vec = model_func(t_vec, 10, 0.01, 1, 12)
    acumm = accum_func(q_vec, elapsed_days)

    fig, ax  = plt.subplots(figsize = [10,5])
    ax.plot(date_vec, q_vec, 'k', linewidth = 2.5)
    ax.set_title('Liquid Production', fontweight = 'bold')
    ax.set_ylabel('Rate, 000 b/d', fontweight = 'bold')
    ax.set_xlabel('Date', fontweight = 'bold')

    axb = ax.twinx()
    axb.plot(date_vec, acumm, 'k', linewidth = 2.5)
    axb.set_ylabel('Cummulative, 000 b/d', fontweight = 'bold')
    plt.tight_layout()
    plt.show()

'''