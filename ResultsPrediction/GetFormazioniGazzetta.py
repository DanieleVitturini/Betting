# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:21:45 2020

@author: Daniele
"""

from bs4 import BeautifulSoup
import urllib.request
import re

import numpy as np
import pandas as pd

#Gazzetta
url = "https://www.gazzetta.it/Calcio/prob_form/"
try:
 page = urllib.request.urlopen(url)
except:
 print("An error occured.")
soup = BeautifulSoup(page, "html.parser")

print(soup.text)

#cercando team trova anche le partite
regex = re.compile("team")
content_lis = soup.find_all("span", attrs={"class":regex})

print(content_lis)
#Pulire file
content = []
for li in content_lis:
    content.append(li.getText().replace("\n","").replace("\t",""))
print(content)

#Crea lista squadre
N_Squadre = 20
N_giocatori = 11

squadre=[]
for i in range(N_Squadre):
    squadre.append(content[i])
    
print(squadre)
arrSquadre=np.array(squadre)
print(arrSquadre)

#pulisco il file dalla lista delle squadre. attenzione, ogni volta rimuove primi 20 elementi,
# se ripetuto il comando va ricominciata la procedura da capo.
for i in range(N_Squadre):
    content.pop(0)
    i+=1
    
print(content)

#creo file squadra=['giocatore1','giocatore2', ecc]
out_df = pd.DataFrame()

for i in range(N_Squadre):
    #formazione_{i}=[]
    lista=[]
    for j in range(N_giocatori):
        x=(i*N_giocatori)+j
        lista.append(content[x])
        #Squadra = arrSquadre[i]
        Squadra = np.array(lista)
        #content.pop(0) 
    squadra = arrSquadre[i]
    out_df[squadra] = pd.Series(Squadra)
    #print(squadra)
    formazione = [Squadra]    
    #print(formazione)
    file= open("roseGazzetta7.txt", "a")
    file.write("{} = {}".format(squadra,lista))
    file.write("\n")
    file.close()

file= open("roseGazzetta7.txt", "r")
print(file.read())
file.close()

out_df.to_excel('rosegazzetta7.xlsx')