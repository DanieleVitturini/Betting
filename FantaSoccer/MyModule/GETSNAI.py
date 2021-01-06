#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 16:55:15 2020

@author: peter
"""


from bs4 import BeautifulSoup
import urllib.request
import re

import pandas as pd

url = "https://www.snai.it/sport/CALCIO/BUNDESLIGA"

try:
 page = urllib.request.urlopen(url)
except:
 print("An error occured.")
soup = BeautifulSoup(page, "html.parser")
print(soup)

regex = re.compile("application")
content_lis = soup.find_all("script", attrs={"type":regex})
print(content_lis)

#elimina extra
content = []
for li in content_lis:
    
    #pulisco meglio di amuchina o della varichina, per prender la quotina per la nostra scommessina
    content.append(li.getText().replace("\n","").replace("\t","").replace("@","").replace("\\","").replace("/","").replace("\"","").replace(":","").replace(".","").replace("type","").replace("context","").replace("httpschemaorg","").replace("SportsEvent","").replace("name","").replace("startDate","").replace("endDate","").replace("imagehttpsstaticsnaiitsitesallmodulescustomsnai_new_homepageimagessnaipng?","").replace("urlhttpswwwsnaiitsport","").replace("c80666ba384434d0fc25fd230935ce98","").replace("description,","").replace("location","").replace("Place,","").replace("identifier","").replace("address","").replace("PostalAddress","").replace("Text","").replace("value","").replace("quote","").replace("1X2","").replace("=>","").replace("SERIE A,","").replace("UDINESE","").replace("FIORENTINA","").replace("MILAN","").replace("GENOA","").replace("JUVENTUS","").replace("INTER","").replace("SASSUOLO","").replace("BRESCIA","").replace("CAGLIARI","").replace("ROMA","").replace("PARMA","").replace("SPAL","").replace("LAZIO","").replace("BOLOGNA","").replace("NAPOLI","").replace("TORINO","").replace("LECCE","").replace("ATALANTA","").replace("SAMPDORIA","").replace("VERONA","").replace("T113000+0100","").replace("T133000+0100","").replace("T140000+0100","").replace("T160000+0100","").replace("T170000+0100","").replace("T190000+0100","").replace("T194500+0100","").replace("T214500+0100","").replace("%","").replace("{","").replace("}","").replace("CALCIOSERIE20A20-20","").replace("2020-02-29","").replace("2020-03-01","").replace("2020-03-02","").replace("300911836","").replace("300911837","").replace("300911838","").replace("300911839","").replace("300911840","").replace("300911841","").replace("300911842","").replace("300911843","").replace("300911844","").replace("300911845","").replace(","," ").replace("-",",").replace("      "," ,").replace("]","").replace("[","").replace(" ",""))
    content.append(li.getText().replace("\n","").replace("\t","").replace("@","").replace("\\","").replace("/","").replace("\"","").replace(":","").replace(".","").replace("type","").replace("context","").replace("httpschemaorg","").replace("SportsEvent","").replace("name","").replace("startDate","").replace("endDate","").replace("imagehttpsstaticsnaiitsitesallmodulescustomsnai_new_homepageimagessnaipng?","").replace("urlhttpswwwsnaiitsport","").replace("c80666ba384434d0fc25fd230935ce98","").replace("description,","").replace("location","").replace("Place,","").replace("identifier","").replace("address","").replace("PostalAddress","").replace("Text","").replace("value","").replace("quote","").replace("1X2","").replace("=>","").replace("BUNDESLIGA,","").replace("BIELEFELD","").replace("MONCHENGLADBACH","").replace("COLONIA","").replace("AUGSBURG","").replace("EINTRACHT FRANKFURT","").replace("LEVERKUSEN","").replace("HOFFENHEIM","").replace("FRIBURGO","").replace("WERDER BREMEN","").replace("UNION BERLINO","").replace("HERTHA","").replace("SCHALKE 04","").replace("STOCCARDA","").replace("LEIPZIG","").replace("T113000+0100","").replace("T133000+0100","").replace("T140000+0100","").replace("T160000+0100","").replace("T170000+0100","").replace("T190000+0100","").replace("T194500+0100","").replace("T214500+0100","").replace("%","").replace("{","").replace("}","").replace("CALCIOSERIE20A20-20","").replace("2020-02-29","").replace("2020-03-01","").replace("2020-03-02","").replace("300911836","").replace("300911837","").replace("300911838","").replace("300911839","").replace("300911840","").replace("300911841","").replace("300911842","").replace("300911843","").replace("300911844","").replace("300911845","").replace(","," ").replace("-",",").replace("      "," ,").replace("]","").replace("[","").replace(" ",""))
    content.append(li.getText())
    
print(content)

culo=(content[0])

quote=culo.split(",")
quote.pop()

HomeTeam=[]
AwayTeam=[]
HomeWin=[]
Draw=[]
AwayWin=[]
uno=[]
ics=[]
due=[]
for g in range(0,10):
    HomeTeam.append(quote.pop(0))
    AwayTeam.append(quote.pop(0))
    uno.append(quote.pop(0))
    ics.append(quote.pop(0))
    due.append(quote.pop(0))
    
uno=list(map(int,uno))
ics=list(map(int,ics))
due=list(map(int,due))

for porcoddio in range(0,10):
    HomeWin.append(uno[porcoddio]/100)
    Draw.append(ics[porcoddio]/100)
    AwayWin.append(due[porcoddio]/100)
    porcoddio+=1
    
out_df = pd.DataFrame()
out_df['HomeTeam'] = pd.Series(HomeTeam)
out_df['AwayTeam'] = pd.Series(AwayTeam)
out_df['HomeWin'] = pd.Series(HomeWin)
out_df['Draw'] = pd.Series(Draw)
out_df['AwayWin'] = pd.Series(AwayWin)

out_df.to_excel('Snai_quotes_8.xlsx')