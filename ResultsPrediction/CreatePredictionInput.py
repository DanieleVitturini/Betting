import pandas as pd
import string

dataset = pd.read_excel('../MediaVoto/Results_Giornata_9_2020.xlsx')

output = pd.DataFrame()

formazioni = pd.read_excel('rosegazzetta9.xlsx')

Atalanta = formazioni['ATA']
Benevento = formazioni['BEN']
Bologna = formazioni['BOL']
Cagliari = formazioni['CAG']
Crotone = formazioni['CRO']
Fiorentina = formazioni['FIO']
Genoa = formazioni['GEN']
Inter = formazioni['INT']
Juventus = formazioni['JUV']
Lazio = formazioni['LAZ']
Milan = formazioni['MIL']
Napoli = formazioni['NAP']
Parma = formazioni['PAR']
Roma = formazioni['ROM']
Sampdoria = formazioni['SAM']
Sassuolo = formazioni['SAS']
Spezia = formazioni['SPE']
Torino = formazioni['TOR']
Udinese = formazioni['UDI']
Verona = formazioni['VER']

Formazioni = {'ATALANTA':Atalanta,'BENEVENTO':Benevento,'BOLOGNA':Bologna,'CAGLIARI':Cagliari,'CROTONE':Crotone,'FIORENTINA':Fiorentina,'GENOA':Genoa,'INTER':Inter,'JUVENTUS':Juventus,'LAZIO':Lazio,'MILAN':Milan, 'NAPOLI':Napoli, 'PARMA':Parma,'ROMA':Roma,'SAMPDORIA':Sampdoria,'SASSUOLO':Sassuolo,'SPEZIA':Spezia,'TORINO':Torino,'UDINESE':Udinese,'VERONA':Verona}
#Casa = ['BRESCIA','BOLOGNA','SPAL','FIORENTINA','GENOA','ATALANTA','TORINO','VERONA','ROMA','INTER']
#Trasferta = ['NAPOLI','UDINESE','JUVENTUS','MILAN','LAZIO','SASSUOLO','PARMA','CAGLIARI','LECCE','SAMPDORIA']

quote = pd.read_excel('Snai_quotes_2020_9.xlsx')
Casa = quote['HomeTeam'].str.upper()
Trasferta = quote['AwayTeam'].str.upper()

HomeMV = []

Giocatori = [' '.join(w for w in a.split() if w.isupper())  for a in dataset['Giocatore']]

dataset['Giocatore'] = Giocatori

dataset = dataset.replace('TROOST-EKONG','EKONG')
dataset = dataset.replace('RODRIGO BECÃO','BECAO')
#dataset = dataset.replace('ZEEGELAAR','ZEEGELAR')
#dataset = dataset.replace('LEIVA','LUCAS LEIVA')
dataset = dataset.replace('IGOR JULIO','IGOR')
dataset = dataset.replace('MARTINEZ','LAUTARO')
#dataset = dataset.replace('LOPEZ','PAU LOPEZ')
dataset = dataset.replace('PERES','BRUNO PERES')
dataset = dataset.replace('ÜNDER','UNDER')
dataset = dataset.replace('DIAZ','BRAHIM DIAZ')
dataset = dataset.replace('ALVES','BRUNO ALVES')
dataset = dataset.replace('NKOULOU',"N'KOULOU")
dataset = dataset.replace('MEITE','MEITÉ')
dataset = dataset.replace("MONTIPO'",'MONTIPÒ')
#dataset = dataset.replace("MARIO RUI",'M. RUI')
dataset = dataset.replace("RUIZ",'FABIAN RUIZ')
dataset = dataset.replace("KOUAMÉ",'KOUAME')
#dataset = dataset.replace("PEZZELLA GER.",'PEZZELLA')
dataset = dataset.replace("SILVA",'A. SILVA')
dataset = dataset.replace("RONALDO",'C. RONALDO')
#dataset = dataset.replace("ZAPATA",'C. ZAPATA')
#dataset = dataset.replace("PELLEGRINI",'LU. PELLEGRINI')
#dataset = dataset.replace('LOPEZ','M. LOPEZ')


for squadra in Casa:
    print(squadra)
    #print(dataset[(dataset['Giocatore'].str.split(' ')[0].isin(Formazioni[squadra])) & (dataset['Squadra']=='LECCE')]['Prediction'])
    num_giocatori = pd.Series(dataset[(dataset['Giocatore'].isin(Formazioni[squadra])) & (dataset['Squadra']==squadra)]['Prediction'].size)
    print(num_giocatori)
    if num_giocatori.iloc[0]!=11:    
        print(pd.Series(dataset[(dataset['Giocatore'].isin(Formazioni[squadra])) & (dataset['Squadra']==squadra)]['Giocatore']))
    somma = pd.Series(dataset[(dataset['Giocatore'].isin(Formazioni[squadra])) & (dataset['Squadra']==squadra)]['Prediction'].mean())
    print(somma)
    HomeMV.append(somma.values[0])

AwayMV = []

for squadra in Trasferta:
    print(squadra)
    #print(dataset[(dataset['Giocatore'].str.split(' ')[0].isin(Formazioni[squadra])) & (dataset['Squadra']=='LECCE')]['Prediction'])
    num_giocatori = pd.Series(dataset[(dataset['Giocatore'].isin(Formazioni[squadra])) & (dataset['Squadra']==squadra)]['Prediction'].size)
    print(num_giocatori)
    if num_giocatori.iloc[0]!=11:    
        print(pd.Series(dataset[(dataset['Giocatore'].isin(Formazioni[squadra])) & (dataset['Squadra']==squadra)]['Giocatore']))
    somma = pd.Series(dataset[(dataset['Giocatore'].isin(Formazioni[squadra])) & (dataset['Squadra']==squadra)]['Prediction'].mean())
    print(somma)
    AwayMV.append(somma.values[0])
    
output['HomeTeam'] = HomeMV
output['AwayTeam'] = AwayMV

output['HomeWin'] = quote['HomeWin']
output['Draw'] = quote['Draw']
output['AwayWin'] = quote['AwayWin']
output['Casa'] = Casa
output['Trasferta'] = Trasferta

output.to_excel('Input_Scommessa_9.xlsx')
