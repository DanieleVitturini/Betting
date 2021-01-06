#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 19:59:59 2021

@author: peter
"""
import pandas as pd
import PredictMV as PMV
import UnderStat as US
import GetLineups as LU
import PredictResult as PR
import GetOdds as GO

giorn = 18
league = 'Ligue1'

xG_ligue1 = US.Get_xGTeams(league)
#US.CreateCalendar(league)

pl_file = PMV.CreatePlayerFile(giorn,league)
team_file = PMV.CreateTeamFile(giorn,league,pl_file)
dCalendar = pd.read_excel('../Calendar'+league+'.xlsx')
pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)

inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
Pred = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)
MLR_result = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)

#Results Prediction
US.Fix_xGFiles(league,dCalendar,giorn)

df_xG_tot,df_xGA_tot = US.Create_xGFiles(league,giorn)

ligue1_lineups = LU.ScrapLineUps(league,giorn)
ligue1_odds = GO.Get888(league,giorn)

ligue1_pred = PR.GetPredFile(giorn,league,MLR_result,ligue1_lineups,ligue1_odds)

ligue1_results = US.CreateResults(league,giorn)

ligue1_results_ML = PR.CreateCalendarInput(league,giorn,ligue1_results)

ligue1_results_ML = ligue1_results_ML[ligue1_results_ML['Giornata']>4]

inML,X,y,cm,kellyTestxG,kellyPredictxG,probabilityxG = PR.KNN(team_file,ligue1_results_ML,df_xG_tot,df_xGA_tot,ligue1_pred)

inML,X,y,cm,kellyTestxG,kellyPredictxG,probabilityxG = PR.RandomForest(team_file,ligue1_results_ML,df_xG_tot,df_xGA_tot,ligue1_pred)

