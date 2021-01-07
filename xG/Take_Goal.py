#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:14:49 2020

@author: peter
"""

import pandas as pd
import math

teams = ['Atalanta','Bologna','Benevento','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Crotone','AC_Milan','Napoli','Parma_Calcio_1913','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']

df = {}

for t in teams:
    df[t] = pd.read_excel("../xG/"+t+"_matches_2020.xlsx").dropna()
    
df_xG_home = pd.DataFrame()
df_xG_home["Team"] = teams

df_xG_away = pd.DataFrame()
df_xG_away["Team"] = teams

df_xG_tot = pd.DataFrame()
df_xG_tot["Team"] = teams

for i in range(1,15):
    
    xG_season_home = []
    xG_season_away = []
    xG_season_tot = []
    
    for t in teams:
        df = pd.read_excel("../xG/"+t+"_matches_2020.xlsx").dropna().head(i)
    
        team = t.replace("_"," ")
        
        home_matches = df[df['home']==team]
        xG_season_home.append(home_matches['goals_home'].sum())
        
        away_matches = df[df['away']==team]
        xG_season_away.append(away_matches['goals_away'].sum())
        
        xG_season_tot.append(home_matches['goals_home'].sum()+away_matches['goals_away'].sum())
        
    df_xG_home["Giornata {0}".format(i+1)] = xG_season_home
    df_xG_away["Giornata {0}".format(i+1)] = xG_season_away
    df_xG_tot["Giornata {0}".format(i+1)] = xG_season_tot
    
df_xG_home.to_excel("goals_home_all.xlsx")
df_xG_away.to_excel("goals_away_all.xlsx")
df_xG_tot.to_excel("goals_tot_all.xlsx")

    xGA_season_home = home_matches['xG_away'].sum()
    goal_season_home = home_matches['goals_home'].sum()
    goalA_season_home = home_matches['goals_away'].sum()
    dev_season_home = (goal_season_home-xG_season_home)/math.sqrt(xG_season_home)
    devA_season_home = (goalA_season_home-xGA_season_home)/math.sqrt(xGA_season_home)
    
    xG_last3_home = home_matches['xG_home'].tail(3).sum()
    xGA_last3_home = home_matches['xG_away'].tail(3).sum()
    goal_last3_home = home_matches['goals_home'].tail(3).sum()
    goal_last3_home = home_matches['goals_home'].tail(3).sum()
    
    away_matches = df[df['away']=="Roma"]
    
    xG_season_away = home_matches['xG_away'].sum()
    xGA_season_away = home_matches['xG_home'].sum()
    
    xG_last3_away = home_matches['xG_away'].tail(3).sum()
    xGA_last3_away = home_matches['xG_home'].tail(3).sum()
    
    last_3 = df.tail(3)
    
    xG_last3 = 0
    xGA_last3 = 0
    
    for index, row in last_3.iterrows():
        if(row['home']=='Roma'):
            xG_last3 += row['xG_home']
            xGA_last3 += row['xG_away']
        else:
            xGA_last3 += row['xG_home']
            xG_last3 += row['xG_away']
