#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:46:46 2020

@author: peter
"""

import pandas as pd
import PredictMV as PMV
import UnderStat as US

giorn = 16
league = 'PremierLeague'

xG_PL = US.Get_xGTeams(league)
US.CreateCalendar(league)


pl_file = PMV.CreatePlayerFile(giorn,league)
#Some teams did't play the first match, the 1st file of Voti needs to be changed manually, otherwise those teams will be ignored (all players == 0)
team_file = PMV.CreateTeamFile(giorn,league,pl_file)
dCalendar = pd.read_excel('../Calendar'+league+'.xlsx')

pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)
#NEXT STEP: mettere pl_file come input dello step successivo e aggiungere league
inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
MLR_result = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)

#Results Prediction
US.Create_xGFiles(league,giorn)