#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:10:07 2021

@author: peter
"""

import pandas as pd
import PredictMV as PMV
import UnderStat as US
import GetLineups as LU
import PredictResult as PR
import GetOdds as GO
import numpy as np
import matplotlib.pyplot as plt  


giorn = 18
league = 'Bundesliga'

xG_seriea = US.Get_xGTeams(league)

#US.CreateCalendar(league)

columns_list = ['Voto FS','Gol_segnati_fs', 'Gol_subiti_fs','Ammonizione', 'Espulsione', 'Rigori_segnati', 'Rigori_sbagliati','Rigori_parati']
pl_file = {}

for c in columns_list:
    print(c)
    pl_file[c] = PMV.CreatePlayerFileVar(giorn,league,c)
    
team_file = PMV.CreateTeamFile(giorn,league,pl_file['Voto FS'])

dCalendar = pd.read_excel('../Calendar'+league+'.xlsx')

pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)
inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
MLR_result,y_test,y_pred,X_test = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file['Voto FS'])

#Results Prediction
US.Fix_xGFiles(league,dCalendar,giorn)

df_xG_tot,df_xGA_tot = US.Create_xGFiles(league,giorn)

seriea_lineups = LU.ScrapLineUps(league,giorn)
seriea_odds = GO.Get888(league,giorn)

#Excluding negative prediction -> need to check Djidji and Luperto
#MLR_result = MLR_result[MLR_result['Prediction']>0]

seriea_pred = PR.GetPredFile(giorn,league,MLR_result,seriea_lineups,seriea_odds,False)

seriea_results = US.CreateResults(league,giorn)

seriea_results_ML = PR.CreateCalendarInput(league,giorn,seriea_results)

seriea_results_ML = seriea_results_ML[seriea_results_ML['Giornata']>4]

#Metodo cut e diff
seriea_pred_diff = seriea_pred.copy()
diff = seriea_pred_diff['HomeTeam'] - seriea_pred_diff['AwayTeam']
seriea_pred_diff.insert(0,'Diff',diff)
seriea_pred_diff = seriea_pred_diff.drop(columns=['HomeTeam','AwayTeam'])

#Cut
diff = seriea_pred['HomeTeam'] - seriea_pred['AwayTeam']
results_pred = diff.apply(PR.ApplyCut)

### ADD PUSHED METHOD ###
########new MLR
new_MLR_result = MLR_result[MLR_result['Prediction']>1]
        
######################
#Sort the predicted data
bins = np.arange(4, 8, 0.25).tolist()
weights = np.ones_like(y_pred)/float(len(y_pred))
(prob_pred, bins_pred, patches) = plt.hist(y_pred, weights=weights,bins=bins)
        
y_test_sort = np.sort(new_MLR_result['Prediction'])
num_pred = len(y_test_sort)
new_y_test = np.empty([0,])
        
for j in range(0,len(prob_pred)):
    print("####")
    print("bin: ",bins_pred[j])
    print("probab: ",prob_pred[j])
    num_exp = int(round(prob_pred[j]*num_pred,0))
    print("number expected: ",num_exp)
    ####
    first_elements = y_test_sort[:num_exp]
    print(first_elements)
    a=np.empty(len(first_elements))
    a.fill(bins_pred[j])
    new_y_test = np.append(new_y_test,a)
    y_test_sort = y_test_sort[num_exp:]
    print(len(y_test_sort))
            
a=np.empty(len(y_test_sort))
a.fill(8)
        
new_y_test = np.append(new_y_test,a)
y_test_sort = np.sort(new_MLR_result['Prediction'])
        
#merge with MLR_result
df_pushed_pred = pd.DataFrame()
df_pushed_pred['Prediction'] = y_test_sort
df_pushed_pred['Pushed_Pred'] = new_y_test
        
new_MLR_result = pd.merge(new_MLR_result,df_pushed_pred,on=['Prediction'])       
new_MLR_result = new_MLR_result.drop(columns=['Prediction'])
new_MLR_result = new_MLR_result.rename(columns={'Pushed_Pred':'Prediction'})

seriea_pred_pushed = PR.GetPredFile(giorn,league,new_MLR_result,seriea_lineups,seriea_odds,False)

#Starting loop on Cannes,Pushup and Diff
df_results_cannes = pd.DataFrame()
df_results_diff = pd.DataFrame()
df_results_pushed = pd.DataFrame()

for j_iter in range (0,10):
    #Cannes
    inML,X,y,cm_rf,kellyTestxG_rf,kellyPredictxG_rf,probabilityxG_rf = PR.RandomForest(team_file,seriea_results_ML,df_xG_tot,df_xGA_tot,seriea_pred)
    df_results_cannes[j_iter] = kellyPredictxG_rf
    
    inML,X,y,cm_rf,kellyTestxG_rf_diff,kellyPredictxG_rf_diff,probabilityxG_rf = PR.RandomForestDiff(team_file,seriea_results_ML,df_xG_tot,df_xGA_tot,seriea_pred_diff)
    df_results_diff[j_iter] = kellyPredictxG_rf_diff
    
    inML,X,y,cm,kellyTestxG_push,kellyPredictxG_push,probabilityxG_push = PR.RandomForest(team_file,seriea_results_ML,df_xG_tot,df_xGA_tot,seriea_pred)    
    df_results_pushed[j_iter] = kellyPredictxG_push

df_results = pd.DataFrame()
df_results['Casa'] = seriea_odds['HomeTeam']
df_results['Trasferta'] = seriea_odds['AwayTeam']
#df_results['Differenza'] = differences_mv[i]
df_results['Cannes'] = df_results_cannes.mode(axis=1)[0]
df_results['Diff'] = df_results_diff.mode(axis=1)[0]
df_results['Cut'] = results_pred
df_results['Pushed'] = df_results_pushed.mode(axis=1)[0]

df_results['Mode 1'] =  df_results[['Cannes','Diff','Cut','Pushed']].mode(axis=1)[0]
df_results['Mode 2'] =  df_results[['Cannes','Diff','Cut','Pushed']].mode(axis=1)[1]


