#Create calendar file with quotes
import pandas as pd
import numpy as np

dataset = pd.read_csv('./SerieA2020.csv')

dataset['HomeTeam'] = dataset['HomeTeam'].str.upper()
dataset['AwayTeam'] = dataset['AwayTeam'].str.upper()

output = pd.DataFrame()
output['HomeTeam'] = dataset['HomeTeam']
output['AwayTeam'] = dataset['AwayTeam']

output['Result'] = 0 #Setting all results to Draw
output.loc[dataset['FTHG']>dataset['FTAG'],'Result']=1 #Setting all home wins to 1
output.loc[dataset['FTHG']<dataset['FTAG'],'Result']=-1 #Setting all away wins to -1

output['B365H'] = dataset['B365H']
output['B365D'] = dataset['B365D']
output['B365A'] = dataset['B365A']

giornate = pd.DataFrame()
giornate['Giornata'] = np.ones(10)

for i in range(2,9):
    print(i)
    nuova_giornata = pd.DataFrame()
    nuova_giornata['Giornata'] = np.ones(10)*i
    giornate = giornate.append(nuova_giornata,ignore_index=True)
    
output['Giornata'] = giornate
output.to_excel('Calendar.xlsx')
