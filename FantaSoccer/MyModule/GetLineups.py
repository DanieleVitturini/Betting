#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:37:27 2020

@author: peter
"""
import pandas as pd# data processing, CSV file I/O (e.g. pd.read_csv) 
import requests 
from bs4 import BeautifulSoup
import numpy as np

def ScrapLineUps(league,giornata):
    if(league=="Bundesliga"):
        url = "https://www.rotowire.com/soccer/lineups.php?league=BUND"
    if(league=="PremierLeague"):
        url = "https://www.rotowire.com/soccer/lineups.php"
    if(league=="SerieA"):
        url = "https://www.rotowire.com/soccer/lineups.php?league=SERI"
    if(league=="Ligue1"):
        url = "https://www.rotowire.com/soccer/lineups.php?league=FRAN"
    res = requests.get(url) 
    soup = BeautifulSoup(res.content, "lxml")
            
    print("Taking link ",url)
    
    Teams = []
    
    for i in range(0,len(soup.findAll('div',class_="lineup__mteam is-home"))):
        Teams.append(soup.findAll('div',class_="lineup__mteam is-home")[i].get_text().replace(" ","").replace("\r","").replace("\n",""))
        Teams.append(soup.findAll('div',class_="lineup__mteam is-visit")[i].get_text().replace(" ","").replace("\r","").replace("\n",""))
    
    out_df = pd.DataFrame()
    counter_pl = 0 #to count the players stored
    counter_team = 0 #to count which team lineup you are taking
    
    lineup = []
    
    for i in range(0,len(soup.findAll('li',class_="lineup__player"))):
        lineup.append(soup.findAll('li',class_="lineup__player")[i].get_text().split("\n")[2])
        counter_pl += 1
        #check if you already got 11 players and switch to new team
        if(counter_pl==11):
            Lineup_team = np.array(lineup)
            out_df[Teams[counter_team]] = pd.Series(Lineup_team)
            lineup = []
            counter_pl = 0
            counter_team += 1
    out_df.to_excel(league+"/Lineups_"+str(giornata)+".xlsx")
    return out_df

def GetRealLineUps(league,giornata):

    if(league=="SerieA"):
        df_voti = pd.read_excel("../Voti/"+league+"/Voti_"+str(giornata)+"a_SerieA.xlsx")
        teams = ['Atalanta','Bologna','Benevento','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Crotone','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']

    df_team = {}    
    out_df = pd.DataFrame()
        
    for t in teams:
        df_team[t] = df_voti[(df_voti['Squadra']==t) & (df_voti['Voto FS']!=0) & (df_voti['Voto FS']!="SV")]
        df_team[t] = df_team[t].replace(np.nan,"")
        
        lineup = []
        
        for index,row in df_team[t].iterrows():
            if(row['Nome']!=""):
                lineup.append(row['Nome']+" "+row['Cognome'])
            else:
                lineup.append(row['Cognome'])
            
        Lineup_team = np.array(lineup)
        out_df[t] = pd.Series(Lineup_team)
    
    out_df = out_df.replace(np.nan,"")    
    out_df.to_excel(league+"/RealLineups_"+str(giornata)+".xlsx") 
    return out_df



