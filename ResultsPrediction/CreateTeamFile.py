# Importing the libraries
import pandas as pd
import numpy as np

dataset = pd.read_excel('../MediaVoto/MediaVoto_giocatori.xlsx')

output = pd.DataFrame()

#Giornate = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
Giornate = np.arange(1,9)
for giorn in Giornate:
    fm = dataset[dataset['Giornata '+str(giorn)]!=0].groupby(['Squadra'])['Giornata '+str(giorn)].mean()
    print(fm)
    output['Giornata '+str(giorn)] = pd.Series(fm)
tot = output.mean(axis=1)
output['Total average '] = pd.Series(tot)

output.to_excel('FantaMedia_Squadre.xlsx')
