#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 18:40:38 2021

@author: peter
"""

import pandas as pd
import PredictMV as PMV
import UnderStat as US
import GetLineups as LU
import PredictResult as PR
import GetOdds as GO

giorn = 16
league = 'SerieA'

xG_seriea = US.Get_xGTeams(league)

#US.CreateCalendar(league)

pl_file = PMV.CreatePlayerFile(giorn,league)

team_file = PMV.CreateTeamFile(giorn,league,pl_file)
dCalendar = pd.read_excel('../Calendar'+league+'.xlsx')
pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)
inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
MLR_result = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)

#Results Prediction
US.Fix_xGFiles(league,dCalendar,giorn)

df_xG_tot,df_xGA_tot = US.Create_xGFiles(league,giorn)

seriea_lineups = LU.ScrapLineUps(league,giorn)
seriea_odds = GO.Get888(league,giorn)

seriea_pred = PR.GetPredFile(giorn,league,MLR_result,seriea_lineups,seriea_odds)

seriea_results = US.CreateResults(league,giorn)

seriea_results_ML = PR.CreateCalendarInput(league,giorn,seriea_results)

seriea_results_ML = seriea_results_ML[seriea_results_ML['Giornata']>4]

inML,X,y,cm,kellyTestxG,kellyPredictxG,probabilityxG = PR.KNN(team_file,seriea_results_ML,df_xG_tot,df_xGA_tot,seriea_pred)

inML,X,y,cm_rf,kellyTestxG_rf,kellyPredictxG_rf,probabilityxG_rf = PR.RandomForest(team_file,seriea_results_ML,df_xG_tot,df_xGA_tot,seriea_pred)
