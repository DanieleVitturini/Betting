# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:45:01 2020

@author: vittu
"""

from bs4 import BeautifulSoup
import urllib.request
import re
import numpy as np
import pandas as pd

url = "https://www.snai.it/sport/CALCIO/SERIE%20A"
try:
 page = urllib.request.urlopen(url)
except:
 print("An error occured.")
soup = BeautifulSoup(page, "html.parser")
#print(soup)

regex = re.compile("application")
content_lis = soup.find_all("script", attrs={"type":regex})
#print(content_lis)

content = []
for li in content_lis:
    
    content.append(li.getText())
#print(content)


#elimina extra
content = []
for li in content_lis:
    #    **************** ATTENZIONE  *******************
    #QUESTA PARTE VA ADATTATA ALLA GIORNATA
    #VANNO INSERITE LE DATE CORRETTE
    #E VANNO INSERITI I NUMERI SERIALI DELLE PARTITE che non si possono prevedere
    #Potrebbe mancare un orario ma dovrei aver messo tutti gli orari possibili
    #pulisco meglio di amuchina o della varichina, per prender la quotina per la nostra scommessina
    content.append(li.getText().replace("\n","").replace("\t","").replace("@","").replace("\\","").replace("/","").replace("\"","").replace(":","").replace(".","").replace("type","").replace("context","").replace("httpschemaorg","").replace("SportsEvent","").replace("name","").replace("startDate","").replace("endDate","").replace("imagehttpsstaticsnaiitsitesallmodulescustomsnai_new_homepageimagessnaipng?","").replace("urlhttpswwwsnaiitsport","").replace("c80666ba384434d0fc25fd230935ce98","").replace("description,","").replace("location","").replace("Place,","").replace("identifier","").replace("address","").replace("PostalAddress","").replace("Text","").replace("value","").replace("quote","").replace("1X2","").replace("=>","").replace("SERIE A,","").replace("UDINESE","").replace("FIORENTINA","").replace("MILAN","").replace("GENOA","").replace("JUVENTUS","").replace("INTER","").replace("SASSUOLO","").replace("BRESCIA","").replace("CAGLIARI","").replace("ROMA","").replace("PARMA","").replace("SPAL","").replace("LAZIO","").replace("BOLOGNA","").replace("NAPOLI","").replace("TORINO","").replace("LECCE","").replace("ATALANTA","").replace("SAMPDORIA","").replace("VERONA","").replace("CROTONE","").replace("BENEVENTO","").replace("SPEZIA","").replace("T113000+0100","").replace("T113036+0100","").replace("T133000+0100","").replace("T133036+0100","").replace("T140000+0100","").replace("T140036+0100","").replace("T160000+0100","").replace("T160036+0100","").replace("T170000+0100","").replace("T173000+0100","").replace("T190000+0100","").replace("T193000+0100","").replace("T194500+0100","").replace("T194536+0100","").replace("T214500+0100","").replace("%","").replace("{","").replace("}","").replace("CALCIOSERIE20A20-20","").replace("CALCIOSERIE20A","").replace("2020-12-05","").replace("2020-12-06","").replace("2020-12-07","").replace("2020-11-30","").replace("304813298","").replace("304813513","").replace("304912680","").replace("304912681","").replace("304912686","").replace("304913232","").replace("304913446","").replace("304913447","").replace("304913766","").replace("304913767","").replace("304914091","").replace("304914092","").replace(","," ").replace("-",",").replace("      "," ,").replace("]","").replace("[","").replace(" ",""))

# ******* PER SISTEMARE SOPRA STAMPA COSA RIMANE ********
#print(content)

#print(content[0])
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

for okaka in range(0,10):
    HomeWin.append(uno[okaka]/100)
    Draw.append(ics[okaka]/100)
    AwayWin.append(due[okaka]/100)
    okaka+=1

d ={'HomeWin':HomeWin, 'Draw':Draw ,'AwayWin':AwayWin , 'Casa':HomeTeam , 'Trasferta':AwayTeam }
out_df = pd.DataFrame(data = d)


print(out_df)

out_df.to_excel('quotesnai10.xlsx')