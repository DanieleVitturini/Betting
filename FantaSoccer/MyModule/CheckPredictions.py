#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:37:19 2021

@author: peter
"""

import pandas as pd
import PredictMV as PMV
import UnderStat as US
import GetLineups as LU
import PredictResult as PR
import GetOdds as GO

giorn = 12
league = "SerieA"

all_vote_cfr = {}

for i in range(9,13):
    giorn = i
    
    real_lu_12 = LU.GetRealLineUps(league,giorn)
    
    pl_file = PMV.CreatePlayerFile(giorn,league)
    
    team_file = PMV.CreateTeamFile(giorn,league,pl_file)
    
    dCalendar = pd.read_excel('../Calendar'+league+'.xlsx')
    pred_file = PMV.CreatePredictionFile(giorn,league,pl_file,team_file,dCalendar)
    
    inputML = PMV.GetMLInput(giorn,league,pl_file,team_file,dCalendar)
    MLR_result = PMV.ML_regress_FS(giorn,league,inputML,pred_file,pl_file)
    
    real_votes = pd.read_excel("../Voti/"+league+"/Voti_"+str(giorn)+"a_SerieA.xlsx")
    real_votes = real_votes[(real_votes['Voto FS']!=0) & (real_votes['Voto FS']!='SV')]
    
    vote_cfr = pd.merge(MLR_result[['CodiceCalciatore','Prediction']],real_votes[['CodiceCalciatore','Cognome','Nome','Ruolo','Squadra','Voto FS']],on=['CodiceCalciatore'],how='inner')
    
    vote_cfr = vote_cfr.drop_duplicates(keep="first")

    all_vote_cfr[i] = vote_cfr