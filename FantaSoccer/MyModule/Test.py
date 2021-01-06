#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:25:13 2020

@author: peter
"""
import pandas as pd
import PredictMV as PMV
import PredictResult as PR

giorn = 12
league = 'SerieA'

pl_file = PMV.CreatePlayerFile(giorn,league)
team_file = PMV.CreateTeamFile(giorn,league,pl_file)
dCalendar = pd.read_excel('../CalendarSerieA.xlsx')
pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)
#NEXT STEP: mettere pl_file come input dello step successivo e aggiungere league
inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
MLR_result = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)

#RESULTS PREDICTION
input_bet = PR.GetPredFile(giorn)
