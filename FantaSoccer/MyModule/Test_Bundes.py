#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 13:44:01 2020

@author: peter
"""

import pandas as pd
import PredictMV as PMV
import UnderStat as US
import GetLineups as LU
import PredictResult as PR
import GetOdds as GO

giorn = 14
league = 'Bundesliga'

#xG_Bundes = US.Get_xGTeams(league)
US.CreateCalendar(league)

pl_file = PMV.CreatePlayerFile(giorn,league)

team_file = PMV.CreateTeamFile(giorn,league,pl_file)
dCalendar = pd.read_excel('../Calendar'+league+'.xlsx')

pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)
#NEXT STEP: mettere pl_file come input dello step successivo e aggiungere league
inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
MLR_result = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)

#Results Prediction
US.Fix_xGFiles(league,dCalendar)
df_xG_tot,df_xGA_tot = US.Create_xGFiles(league,giorn)
bundes_lineups = LU.ScrapLineUps(league,giorn)
bundes_odds = GO.Get888(league,giorn)

bundes_pred = PR.GetPredFile(giorn,league,MLR_result,bundes_lineups,bundes_odds)
bundes_results = US.CreateResults(league)
bundes_results_ML = PR.CreateCalendarInput(league,giorn,bundes_results)

bundes_results_ML = bundes_results_ML[bundes_results_ML['Giornata']>4]
inML,X,y,cm,kellyTestxG,kellyPredictxG,probabilityxG = PR.KNN(team_file,bundes_results_ML,df_xG_tot,df_xGA_tot,bundes_pred)



