#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 15:52:20 2021

@author: peter
"""

from soccerapi.api import Api888Sport
import pandas as pd

def Get888(league,giornata):
    url = ''
    num_matches = 0
    
    api = Api888Sport()
    if(league=="Bundesliga"):
        url = 'https://www.888sport.com/#/filter/football/germany/bundesliga'
        num_matches = 9
    if(league=="SerieA"):
        url = 'https://www.888sport.com/#/filter/football/italy/serie_a'
        num_matches = 10
    if(league=="Ligue1"):
        url = 'https://www.888sport.com/#/filter/football/france/ligue_1'
        num_matches=10
    odds = api.odds(url)
    odds = odds[:num_matches]
    
    home_team = []
    away_team = []
    home_win = []
    draw = []
    away_win = []
    for o in odds:
        home_team.append(o['home_team'])
        away_team.append(o['away_team'])
        home_win.append(o['full_time_resut']['1'])
        away_win.append(o['full_time_resut']['2'])
        draw.append(o['full_time_resut']['X'])
    df = pd.DataFrame()
    df['HomeTeam'] = home_team
    df['AwayTeam'] = away_team
    df['HomeWin'] = home_win
    df['Draw'] = draw
    df['AwayWin'] = away_win

    #BUNDESLIGA
    df = df.replace('Borussia Mönchengladbach','Borussia MGladbach')
    df = df.replace('1. FC Köln','Colonia')
    df = df.replace('FC Augsburg','Augsburg')
    df = df.replace('1. FC Union Berlin','Union Berlino')
    df = df.replace('Werder Bremen','Werder Brema')
    df = df.replace('Eintracht Frankfurt','Eintracht Francoforte')
    df = df.replace('Bayer Leverkusen','Leverkusen')
    df = df.replace('TSG Hoffenheim','Hoffenheim')
    df = df.replace('SC Freiburg','Friburgo')
    df = df.replace('Hertha BSC','Hertha')
    df = df.replace('FC Schalke 04','Schalke 04')
    df = df.replace('VfB Stuttgart','Stoccarda')
    df = df.replace('RB Leipzig','RB Lipsia')
    df = df.replace('VfL Wolfsburg','Wolfsburg')
    df = df.replace('Bayern Munich','Bayern Monaco')
    df = df.replace('Mainz 05','Mainz')
    #SERIEA
    df = df.replace("AC Milan","Milan")
    df = df.replace("Hellas Verona","Verona")
    #LIGUE1
    df = df.replace("Nice","Nizza")
    df = df.replace("Strasbourg","Strasburgo")
    df = df.replace("Nîmes Olympique","Nimes")
    df = df.replace("Saint-Étienne","Saint-Etienne")
    df = df.replace("Paris SG","PSG")
    df = df.replace("Marseille","Marsiglia")
    df = df.replace("Lyon","Lione")
    df = df.replace("Dijon","Digione")
    
    df.to_excel(league+"/Odds_giornata_"+str(giornata)+".xlsx")
    return df