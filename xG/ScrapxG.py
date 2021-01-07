import numpy as np# linear algebra 
import pandas as pd# data processing, CSV file I/O (e.g. pd.read_csv) 
import requests 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json 

team_list = ['Atalanta','Bologna','Benevento','Cagliari','Fiorentina','Genoa','Inter','Juventus','Lazio','Spezia','AC_Milan','Napoli','Parma_Calcio_1913','Roma','Sampdoria','Sassuolo','Crotone','Torino','Udinese','Verona']

for team in team_list:
    url = "https://understat.com/team/"+team+"/2020"
    res = requests.get(url) 
    soup = BeautifulSoup(res.content, "lxml")
    
    scripts = soup.find_all('script')
    
    string_with_json_obj = '' 
    cont = []
    
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
    
    df_out.to_excel("../xG/"+team+"_matches_2020.xlsx")

