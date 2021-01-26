#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 12:03:10 2020

@author: peter
"""

import pandas as pd# data processing, CSV file I/O (e.g. pd.read_csv) 
import requests 
from bs4 import BeautifulSoup
import json 
import numpy as np
import math

base_url = 'https://understat.com/league'

def FixTeamName(df,columns):
    
    df = df.replace('Arminia_Bielefeld','Arminia Bielefeld')
    df = df.replace('Bayer_Leverkusen','Leverkusen')
    df = df.replace('Bayern_Munich','Bayern Monaco')
    df = df.replace('Borussia_Dortmund','Borussia Dortmund')
    df = df.replace('Borussia_M.Gladbach','Borussia MGladbach')
    df = df.replace('Eintracht_Frankfurt','Eintracht Francoforte')
    df = df.replace('FC_Cologne','Colonia')
    df = df.replace('Freiburg','Friburgo')
    df = df.replace('Hertha_Berlin','Hertha')
    df = df.replace('Mainz_05','Mainz')
    df = df.replace('RasenBallsport_Leipzig','RB Lipsia')
    df = df.replace('Schalke_04','Schalke 04')
    df = df.replace('Union_Berlin','Union Berlino')
    df = df.replace('VfB_Stuttgart','Stoccarda')
    df = df.replace('Werder_Bremen','Werder Brema')
    
    #results file
    df = df.replace('Eintracht Frankfurt','Eintracht Francoforte')
    df = df.replace('Union Berlin','Union Berlino')
    df = df.replace('Bayer Leverkusen','Leverkusen')
    df = df.replace('Bayern Munich','Bayern Monaco')
    df = df.replace('Borussia M.Gladbach','Borussia MGladbach')
    df = df.replace('FC Cologne','Colonia')
    df = df.replace('VfB Stuttgart','Stoccarda')
    df = df.replace('Werder Bremen','Werder Brema')
    df = df.replace('RasenBallsport Leipzig','RB Lipsia')
    df = df.replace('Mainz 05','Mainz')
    df = df.replace('Hertha Berlin','Hertha')
    
    for x in columns:   
        df[x] = df[x].str.upper()
    
    return df

def CreateResults(league,giornata):
    if(league=="Bundesliga"):
       teams = ['Arminia Bielefeld','Augsburg','Leverkusen','Bayern Monaco','Borussia Dortmund','Borussia MGladbach','Eintracht Francoforte','Colonia','Friburgo','Hertha','Hoffenheim','Mainz','RB Lipsia','Schalke 04','Union Berlino','Stoccarda','Werder Brema','Wolfsburg']
    if(league=="SerieA"):
        teams = ['Atalanta','Bologna','Crotone','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Benevento','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="Ligue1"):
        teams = ['Angers','Bordeaux','Brest','Digione','Lens','Lille','Lorient','Lione','Marsiglia','Metz','Monaco','Montpellier','Nantes','Nizza','Nimes','PSG','Reims','Rennes','Saint-Etienne','Strasburgo']
    if(league=="Liga"):
        teams = ['Alaves','Athletic Bilbao','Atletico Madrid','Barcellona','Cadiz','Celta Vigo','Eibar','Elche CF','Getafe','Granada CF','Levante','CA Osasuna','Betis','Real Madrid','Real Sociedad','Valladolid','Huesca','Siviglia','Valencia','Villarreal']

    df = {}
    
    for t in teams:
        df[t] = pd.read_excel("../xG/"+league+"/"+t+"_matches_2020_fixed.xlsx").dropna()
       
    rounds = {}
    output = pd.DataFrame()
    
    for i in range(0,giornata-1):
        matches = pd.DataFrame()
        for t in teams:
            matches = matches.append(df[t].loc[[i]])
        matches = matches.drop_duplicates(subset = ['home'],keep='first')
        rounds[i] = (matches)
        output = output.append(matches)
        
    output = FixTeamName(output,['home','away'])
    output.to_excel(league+"/Results2020_until_round_"+str(giornata)+".xlsx")
    output['Giornata'] = output.index+1
    return output
    
def Create_xGFiles(league,giornata):
    
    if(league=="SerieA"):
        teams = ['Atalanta','Bologna','Benevento','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Crotone','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="PremierLeague"):
        print("Getting PremierLeague xG")
        teams = ['Arsenal','Aston_Villa','Brighton','Burnley','Chelsea','Crystal_Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester_City','Manchester_United','Newcastle_United','Sheffield_United','Southampton','Tottenham','West_Bromwich_Albion','West_Ham','Wolverhampton_Wanderers']
    if(league=="Bundesliga"):
        teams = ['Arminia Bielefeld','Augsburg','Leverkusen','Bayern Monaco','Borussia Dortmund','Borussia MGladbach','Eintracht Francoforte','Colonia','Friburgo','Hertha','Hoffenheim','Mainz','RB Lipsia','Schalke 04','Union Berlino','Stoccarda','Werder Brema','Wolfsburg']
    if(league=="Ligue1"):
        teams = ['Angers','Bordeaux','Brest','Digione','Lens','Lille','Lorient','Lione','Marsiglia','Metz','Monaco','Montpellier','Nantes','Nizza','Nimes','PSG','Reims','Rennes','Saint-Etienne','Strasburgo']
    if(league=="Liga"):
        teams = ['Alaves','Athletic Bilbao','Atletico Madrid','Barcellona','Cadiz','Celta Vigo','Eibar','Elche CF','Getafe','Granada CF','Levante','CA Osasuna','Betis','Real Madrid','Real Sociedad','Valladolid','Huesca','Siviglia','Valencia','Villarreal']


    df_xG_home = pd.DataFrame()
    df_xG_home["Team"] = teams
    
    df_xG_away = pd.DataFrame()
    df_xG_away["Team"] = teams
    
    df_xG_tot = pd.DataFrame()
    df_xG_tot["Team"] = teams
    
    df_xGA_home = pd.DataFrame()
    df_xGA_home["Team"] = teams
    
    df_xGA_away = pd.DataFrame()
    df_xGA_away["Team"] = teams
    
    df_xGA_tot = pd.DataFrame()
    df_xGA_tot["Team"] = teams
    
    for i in range(1,giornata):
        
        xG_season_home = []
        xG_season_away = []
        xG_season_tot = []
        xGA_season_home = []
        xGA_season_away = []
        xGA_season_tot = []
        
        for t in teams:
            df = pd.read_excel("../xG/"+league+"/"+t+"_matches_2020_fixed.xlsx").dropna().head(i)
        
            team = t.replace("_"," ")
            
            home_matches = df[df['home']==team]
            xG_season_home.append(home_matches['xG_home'].sum())
            xGA_season_home.append(home_matches['xG_away'].sum())
            
            away_matches = df[df['away']==team]
            xG_season_away.append(away_matches['xG_away'].sum())
            xGA_season_away.append(away_matches['xG_home'].sum())
            
            xG_season_tot.append(home_matches['xG_home'].sum()+away_matches['xG_away'].sum())
            xGA_season_tot.append(home_matches['xG_away'].sum()+away_matches['xG_home'].sum())
            
        df_xG_home["Giornata {0}".format(i+1)] = xG_season_home
        df_xG_away["Giornata {0}".format(i+1)] = xG_season_away
        df_xG_tot["Giornata {0}".format(i+1)] = xG_season_tot
        df_xGA_home["Giornata {0}".format(i+1)] = xGA_season_home
        df_xGA_away["Giornata {0}".format(i+1)] = xGA_season_away
        df_xGA_tot["Giornata {0}".format(i+1)] = xGA_season_tot
    
    df_xG_home = FixTeamName(df_xG_home,['Team'])
    df_xG_away = FixTeamName(df_xG_away,['Team'])
    df_xG_tot = FixTeamName(df_xG_tot,['Team'])
    df_xGA_home = FixTeamName(df_xGA_home,['Team'])
    df_xGA_away = FixTeamName(df_xGA_away,['Team'])
    df_xGA_tot = FixTeamName(df_xGA_tot,['Team'])
    
    df_xG_home.to_excel(league+"/xG_home_all_"+str(giornata)+".xlsx")
    df_xG_away.to_excel(league+"/xG_away_all_"+str(giornata)+".xlsx")
    df_xG_tot.to_excel(league+"/xG_tot_all_"+str(giornata)+".xlsx")
    df_xGA_home.to_excel(league+"/xGA_home_all_"+str(giornata)+".xlsx")
    df_xGA_away.to_excel(league+"/xGA_away_all_"+str(giornata)+".xlsx")
    df_xGA_tot.to_excel(league+"/xGA_tot_all_"+str(giornata)+".xlsx")
    
    return df_xG_tot,df_xGA_tot
    
def Get_xGTeams(league):
    
    team_list = []
    if(league=="SerieA"):
        print("Getting SerieA xG")
        team_list = ['Atalanta','Bologna','Crotone','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Benevento','AC_Milan','Napoli','Parma_Calcio_1913','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="PremierLeague"):
        print("Getting PremierLeague xG")
        team_list = ['Arsenal','Aston_Villa','Brighton','Burnley','Chelsea','Crystal_Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester_City','Manchester_United','Newcastle_United','Sheffield_United','Southampton','Tottenham','West_Bromwich_Albion','West_Ham','Wolverhampton_Wanderers']
    if(league=="Bundesliga"):
        team_list = ['Arminia_Bielefeld','Augsburg','Bayer_Leverkusen','Bayern_Munich','Borussia_Dortmund','Borussia_M.Gladbach','Eintracht_Frankfurt','FC_Cologne','Freiburg','Hertha_Berlin','Hoffenheim','Mainz_05','RasenBallsport_Leipzig','Schalke_04','Union_Berlin','VfB_Stuttgart','Werder_Bremen','Wolfsburg']
    if(league=="Ligue1"):
        team_list = ['Angers','Bordeaux','Brest','Dijon','Lens','Lille','Lorient','Lyon','Marseille','Metz','Monaco','Montpellier','Nantes','Nice','Nimes','Paris Saint Germain','Reims','Rennes','Saint-Etienne','Strasbourg']
    if(league=="Liga"):
        team_list = ['Alaves','Athletic_Club','Atletico_Madrid','Barcelona','Cadiz','Celta_Vigo','Eibar','Elche','Getafe','Granada','Levante','Osasuna','Real_Betis','Real_Madrid','Real_Sociedad','Real_Valladolid','SD_Huesca','Sevilla','Valencia','Villarreal']
    for team in team_list:
        url = "https://understat.com/team/"+team+"/2020"
        res = requests.get(url) 
        soup = BeautifulSoup(res.content, "lxml")
        
        scripts = soup.find_all('script')
        
        string_with_json_obj = '' 
        cont = []
        print(url)
        for el in scripts: 
            cont.append(el.contents)
            if 'datesData' in el.contents: 
                print("FOUND!")
            #    string_with_json_obj = el.text.strip()
        string_with_json_obj = cont[1][0]
                
        ind_start = string_with_json_obj.index("('")+2 
        ind_end = string_with_json_obj.index("')") 
        json_data = string_with_json_obj[ind_start:ind_end] 
        json_data = json_data.encode('utf8').decode('unicode_escape')
        
        data = json.loads(json_data)
        
        df = pd.DataFrame(data)
        
        home = []
        away = []
        xG_h = []
        xG_a = []
        goals_h = []
        goals_a = []
        
        for row in df.iterrows():
            home.append(row[1]['h']['title'])
            away.append(row[1]['a']['title'])
            xG_h.append(row[1]['xG']['h'])
            xG_a.append(row[1]['xG']['a'])
            goals_h.append(row[1]['goals']['h'])
            goals_a.append(row[1]['goals']['a'])
        df_out = pd.DataFrame()
        df_out['home'] = home
        df_out['away'] = away
        df_out['xG_home'] = xG_h
        df_out['xG_away'] = xG_a
        df_out['goals_home'] = goals_h
        df_out['goals_away'] = goals_a
        
        df_out.to_excel("../xG/"+league+"/"+team+"_matches_2020.xlsx")
    return 1

def CreateCalendar(league):
    
    team_list = []
    if(league=="SerieA"):
        print("Getting SerieA xG")
        team_list = ['Atalanta','Bologna','Crotone','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Benevento','AC_Milan','Napoli','Parma_Calcio_1913','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="PremierLeague"):
        print("Getting PremierLeague xG")
        team_list = ['Arsenal','Aston_Villa','Brighton','Burnley','Chelsea','Crystal_Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester_City','Manchester_United','Newcastle_United','Sheffield_United','Southampton','Tottenham','West_Bromwich_Albion','West_Ham','Wolverhampton_Wanderers']
    if(league=="Bundesliga"):
        team_list = ['Arminia_Bielefeld','Augsburg','Bayer_Leverkusen','Bayern_Munich','Borussia_Dortmund','Borussia_M.Gladbach','Eintracht_Frankfurt','FC_Cologne','Freiburg','Hertha_Berlin','Hoffenheim','Mainz_05','RasenBallsport_Leipzig','Schalke_04','Union_Berlin','VfB_Stuttgart','Werder_Bremen','Wolfsburg']
    if(league=="Ligue1"):
        team_list = ['Angers','Bordeaux','Brest','Dijon','Lens','Lille','Lorient','Lyon','Marseille','Metz','Monaco','Montpellier','Nantes','Nice','Nimes','Paris Saint Germain','Reims','Rennes','Saint-Etienne','Strasbourg']
    if(league=="Liga"):
        team_list = ['Alaves','Athletic_Club','Atletico_Madrid','Barcelona','Cadiz','Celta_Vigo','Eibar','Elche','Getafe','Granada','Levante','Osasuna','Real_Betis','Real_Madrid','Real_Sociedad','Real_Valladolid','SD_Huesca','Sevilla','Valencia','Villarreal']

    output = pd.DataFrame()
    
    for t in team_list:
        df = pd.read_excel("../xG/"+league+"/"+t+"_matches_2020.xlsx")
        opponent = []
        isHome = []
        t = t.replace("_"," ")
        for index,row in df.iterrows():
            print(row['home'])
            if(row['home']==t):
                isHome.append(1)
                opponent.append(row['away'].upper())
            else:
                isHome.append(0)
                opponent.append(row['home'].upper())
        
        team_text = t
        #Fixing some teams names which don't match in the columns names
        #SERIE A
        if(t=="Parma Calcio 1913"):
            team_text="Parma"
        if(t=="AC Milan"):
            team_text="Milan"
        #PREMIER LEAGUE
        if(t=="Wolverhampton Wanderers"):
            team_text = "Wolverhampton"
        if(t=="Brighton"):
            team_text = "Brighton Hove"    
        if(t=="Leicester"):
            team_text = "Leicester City"  
        if(t=="Leeds"):
            team_text = "Leeds United" 
        if(t=="West Bromwich Albion"): 
            team_text = "West Bromwich" 
        if(t=="Newcastle United"): 
            team_text = "Newcastle" 
        #BUNDESLIGA
        if(t=="Bayern Munich"): 
            team_text = "Bayern Monaco" 
        if(t=="Borussia M.Gladbach"): 
            team_text = "Borussia MGladbach" 
        if(t=="FC Cologne"): 
            team_text = "Colonia" 
        if(t=="Eintracht Frankfurt"): 
            team_text = "Eintracht Francoforte" 
        if(t=="Freiburg"): 
            team_text = "Friburgo" 
        if(t=="Hertha Berlin"): 
            team_text = "Hertha" 
        if(t=="Bayer Leverkusen"): 
            team_text = "Leverkusen"
        if(t=="Mainz 05"): 
            team_text = "Mainz"
        if(t=="RasenBallsport Leipzig"): 
            team_text = "RB Lipsia"
        if(t=="VfB Stuttgart"): 
            team_text = "Stoccarda"
        if(t=="Union Berlin"): 
            team_text = "Union Berlino"
        if(t=="Werder Bremen"): 
            team_text = "Werder Brema"
        #LIGA    
        output[team_text.upper()+"Opponent"] = opponent
        output[team_text.upper()+"IsHome"] = isHome
    #and inside the dataframe (need to change both!!)
    #SERIE A
    output = output.replace("AC MILAN","MILAN")
    output = output.replace("PARMA CALCIO 1913","PARMA")
    #PREMIER LEAGUE
    output = output.replace("WOLVERHAMPTON WANDERERS","WOLVERHAMPTON")
    output = output.replace("BRIGHTON","BRIGHTON HOVE")
    output = output.replace("LEEDS","LEEDS UNITED")
    output = output.replace("LEICESTER","LEICESTER CITY")
    output = output.replace("WEST BROMWICH ALBION","WEST BROMWICH")
    output = output.replace("NEWCASTLE UNITED","NEWCASTLE")
    #BUNDESLIGA
    output = output.replace("BAYERN MUNICH","BAYERN MONACO")
    output = output.replace("BORUSSIA M.GLADBACH","BORUSSIA MGLADBACH")
    output = output.replace("FC COLOGNE","COLONIA")
    output = output.replace("EINTRACHT FRANKFURT","EINTRACHT FRANCOFORTE")
    output = output.replace("FREIBURG","FRIBURGO")
    output = output.replace("HERTHA BERLIN","HERTHA")
    output = output.replace("BAYER LEVERKUSEN","LEVERKUSEN")
    output = output.replace("MAINZ 05","MAINZ")
    output = output.replace("RASENBALLSPORT LEIPZIG","RB LIPSIA")
    output = output.replace("VFB STUTTGART","STOCCARDA")
    output = output.replace("UNION BERLIN","UNION BERLINO")
    output = output.replace("WERDER BREMEN","WERDER BREMA")
    
    output.to_excel("../Calendar"+league+".xlsx")  
    
def Fix_xGFiles(league,dCalendar,giornata):
    if(league=="SerieA"):
        team_list = ['Atalanta','Bologna','Crotone','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Benevento','AC_Milan','Napoli','Parma_Calcio_1913','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="Ligue1"):
        team_list = ['Angers','Bordeaux','Brest','Dijon','Lens','Lille','Lorient','Lyon','Marseille','Metz','Monaco','Montpellier','Nantes','Nice','Nimes','Paris Saint Germain','Reims','Rennes','Saint-Etienne','Strasbourg']
    if(league=="Bundesliga"):
        team_list = ['Arminia_Bielefeld','Augsburg','Bayer_Leverkusen','Bayern_Munich','Borussia_Dortmund','Borussia_M.Gladbach','Eintracht_Frankfurt','FC_Cologne','Freiburg','Hertha_Berlin','Hoffenheim','Mainz_05','RasenBallsport_Leipzig','Schalke_04','Union_Berlin','VfB_Stuttgart','Werder_Bremen','Wolfsburg']
    if(league=="Liga"):
        team_list = ['Alaves','Athletic_Club','Atletico_Madrid','Barcelona','Cadiz','Celta_Vigo','Eibar','Elche','Getafe','Granada','Levante','Osasuna','Real_Betis','Real_Madrid','Real_Sociedad','Real_Valladolid','SD_Huesca','Sevilla','Valencia','Villarreal']

    for t in team_list:
        old_xG = pd.read_excel('../xG/'+league+'/'+t+'_matches_2020.xlsx')
    
        #SERIE A
        old_xG = old_xG.replace("AC Milan","Milan")
        old_xG = old_xG.replace("Parma Calcio 1913","Parma")
        #LIGUE 1
        old_xG = old_xG.replace("Dijon","Digione")
        old_xG = old_xG.replace("Lyon","Lione")
        old_xG = old_xG.replace("Marseille","Marsiglia")
        old_xG = old_xG.replace("Nice","Nizza")
        old_xG = old_xG.replace("Paris Saint Germain","PSG")
        old_xG = old_xG.replace("Strasbourg","Strasburgo")
        #BUNDESLIGA
        old_xG = old_xG.replace("Bayern Munich","Bayern Monaco")
        old_xG = old_xG.replace("Borussia M.Gladbach","Borussia MGladbach")
        old_xG = old_xG.replace("FC Cologne","Colonia")
        old_xG = old_xG.replace("Eintracht Frankfurt","Eintracht Francoforte")
        old_xG = old_xG.replace("Freiburg","Friburgo")
        old_xG = old_xG.replace("Hertha Berlin","Hertha")
        old_xG = old_xG.replace("Bayer Leverkusen","Leverkusen")
        old_xG = old_xG.replace("Mainz 05","Mainz")
        old_xG = old_xG.replace("RasenBallsport Leipzig","RB Lipsia")
        old_xG = old_xG.replace("VfB Stuttgart","Stoccarda")
        old_xG = old_xG.replace("Union Berlin","Union Berlino")
        old_xG = old_xG.replace("Werder Bremen","Werder Brema")
        #LIGA
        old_xG = old_xG.replace('Athletic Club','Athletic Bilbao')
        old_xG = old_xG.replace('Barcelona','Barcellona')
        old_xG = old_xG.replace('Real Betis','Betis')
        old_xG = old_xG.replace('Osasuna','CA Osasuna')
        old_xG = old_xG.replace('Elche','Elche CF')
        old_xG = old_xG.replace('Granada','Granada CF')
        old_xG = old_xG.replace('SD Huesca','Huesca')
        old_xG = old_xG.replace('Sevilla','Siviglia')
        old_xG = old_xG.replace('Real Valladolid','Valladolid')
        
        if t =='Athletic_Club':
            t = 'Athletic Bilbao'
        if t =='Barcelona':
            t = 'Barcellona'
        if t =='Real_Betis':
            t = 'Betis'  
        if t =='Osasuna':
            t = 'CA Osasuna'
        if t =='Elche':
            t = 'Elche CF'
        if t =='Granada':
            t = 'Granada CF'
        if t =='SD_Huesca':
            t = 'Huesca'
        if t =='Sevilla':
            t = 'Siviglia'
        if t =='Real_Valladolid':
            t = 'Valladolid'
        if t =='Atletico_Madrid':
            t = 'Atletico Madrid'
        if t =='Real_Madrid':
            t = 'Real Madrid'
        if t =='Celta_Vigo':
            t = 'Celta Vigo'
        if t =='Real_Sociedad':
            t = 'Real Sociedad'
        if t=='AC_Milan':
            t = 'Milan'
        if t=='Parma_Calcio_1913':
            t = 'Parma'
        if t=='Dijon':
            t = 'Digione'
        if t=='Lyon':
            t = 'Lione'
        if t=='Marseille':
            t = 'Marsiglia'
        if t=='Nice':
            t = 'Nizza'
        if t=='Paris Saint Germain':
            t = 'PSG'
        if t=='Strasbourg':
            t = 'Strasburgo'
        if(t=="Bayern_Munich"): 
            t = "Bayern Monaco" 
        if(t=="Borussia_M.Gladbach"): 
            t = "Borussia MGladbach" 
        if(t=="FC_Cologne"): 
            t = "Colonia" 
        if(t=="Eintracht_Frankfurt"): 
            t = "Eintracht Francoforte" 
        if(t=="Freiburg"): 
            t = "Friburgo" 
        if(t=="Hertha_Berlin"): 
            t = "Hertha" 
        if(t=="Bayer_Leverkusen"): 
            t = "Leverkusen"
        if(t=="Mainz_05"): 
            t = "Mainz"
        if(t=="RasenBallsport_Leipzig"): 
            t = "RB Lipsia"
        if(t=="VfB_Stuttgart"): 
            t = "Stoccarda"
        if(t=="Union_Berlin"): 
            t = "Union Berlino"
        if(t=="Werder_Bremen"): 
            t = "Werder Brema"
        if (t=="Arminia_Bielefeld"):
            t = "Arminia Bielefeld"
        if (t=="Borussia_Dortmund"):
            t = "Borussia Dortmund"
        if (t=="Schalke_04"):
            t = "Schalke 04"
        new_home = []
        new_away = []
        new_xG_h = []
        new_xG_a = []
        new_goals_h = []
        new_goals_a = []
        
        for index,row in dCalendar.iterrows():
            opp = row[t.upper()+'Opponent']
            isHome = row[t.upper()+'IsHome']
            if(isHome):
                print(t)
                print(opp)
                new_home.append(t)
                new_away.append(old_xG[old_xG['away'].str.upper()==opp]['away'].iloc[0])
                #fix for shifted matches which don't have data yet
                if(giornata>index+1 and math.isnan(old_xG[old_xG['away'].str.upper()==opp]['xG_home'].iloc[0])):
                    new_xG_h.append(0)
                    new_xG_a.append(0)
                    new_goals_h.append(0)
                    new_goals_a.append(0)
                else:
                    new_xG_h.append(old_xG[old_xG['away'].str.upper()==opp]['xG_home'].iloc[0])
                    new_xG_a.append(old_xG[old_xG['away'].str.upper()==opp]['xG_away'].iloc[0])
                    new_goals_h.append(old_xG[old_xG['away'].str.upper()==opp]['goals_home'].iloc[0])
                    new_goals_a.append(old_xG[old_xG['away'].str.upper()==opp]['goals_away'].iloc[0])
            else:
                print(t)
                print(opp)
                new_away.append(t)
                new_home.append(old_xG[old_xG['home'].str.upper()==opp]['home'].iloc[0])
                #fix for shifted matches which don't have data yet
                if(giornata>index+1 and math.isnan(old_xG[old_xG['home'].str.upper()==opp]['xG_home'].iloc[0])):
                    new_xG_h.append(0)
                    new_xG_a.append(0)
                    new_goals_h.append(0)
                    new_goals_a.append(0)
                else:
                    new_xG_h.append(old_xG[old_xG['home'].str.upper()==opp]['xG_home'].iloc[0])
                    new_xG_a.append(old_xG[old_xG['home'].str.upper()==opp]['xG_away'].iloc[0])
                    new_goals_h.append(old_xG[old_xG['home'].str.upper()==opp]['goals_home'].iloc[0])
                    new_goals_a.append(old_xG[old_xG['home'].str.upper()==opp]['goals_away'].iloc[0])
                    
        new_xG = pd.DataFrame()
        
        new_xG['home'] = new_home
        new_xG['away'] = new_away
        new_xG['xG_home'] = new_xG_h
        new_xG['xG_away'] = new_xG_a
        new_xG['goals_home'] = new_goals_h
        new_xG['goals_away'] = new_goals_a
        
        new_xG.to_excel('../xG/'+league+'/'+t+'_matches_2020_fixed.xlsx')
    
    
    
    
    
    
    
    
    
    
    