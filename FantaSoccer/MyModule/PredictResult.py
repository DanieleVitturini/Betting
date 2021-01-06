#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:41:01 2020

@author: peter
"""

import pandas as pd
import statistics

def GetListLU(league,formazioni):
    Lineups = {}
    if(league=="Bundesliga"):
        
        Bielefeld = formazioni['ArminiaBielefeld']
        Frankfurt = formazioni['EintrachtFrankfurt']
        Leverkusen = formazioni['BayerLeverkusen']
        Colonia = formazioni['1.FCKöln']
        Augsburg = formazioni['FCAugsburg']
        Gladbach = formazioni['Mönchengladbach']
        Hoffenheim = formazioni['1899Hoffenheim']
        Freiburg = formazioni['SCFreiburg']
        Werder = formazioni['WerderBremen']
        Union = formazioni['UnionBerlin']
        Hertha = formazioni['HerthaBSCBerlin']
        Schalke = formazioni['FCSchalke04']
        Stuttgart = formazioni['VfBStuttgart']
        RBLeipzig = formazioni['RBLeipzig']
        Dortmund = formazioni['BorussiaDortmund']
        Wolfsburg = formazioni['VfLWolfsburg']
        Bayern = formazioni['BayernMunich']
        Mainz = formazioni['FSVMainz05']
        Lineups = {'ARMINIA BIELEFELD':Bielefeld,'AUGSBURG':Augsburg,'BAYERN MONACO':Bayern,'BORUSSIA DORTMUND':Dortmund,'BORUSSIA MGLADBACH':Gladbach,'COLONIA':Colonia,'EINTRACHT FRANCOFORTE':Frankfurt,'FRIBURGO':Freiburg,'HERTHA':Hertha,'HOFFENHEIM':Hoffenheim,'LEVERKUSEN':Leverkusen,'MAINZ':Mainz,'RB LIPSIA':RBLeipzig,'SCHALKE 04':Schalke,'STOCCARDA':Stuttgart,'UNION BERLINO':Union,'WERDER BREMA':Werder,'WOLFSBURG':Wolfsburg}
    
    if(league=="SerieA"):
        Atalanta = formazioni['Atalanta']
        Benevento = formazioni['Benevento']
        Bologna  = formazioni['Bologna']
        Cagliari  = formazioni['Cagliari']
        Crotone  = formazioni['Crotone']
        Fiorentina = formazioni['Fiorentina']
        Genoa = formazioni['Genoa']
        Inter = formazioni['InterMilan']
        Juventus = formazioni['Juventus']
        Lazio = formazioni['Lazio']
        Milan = formazioni['ACMilan']
        Napoli = formazioni['Napoli']
        Parma = formazioni['Parma']
        Roma = formazioni['Roma']
        Sampdoria = formazioni['Sampdoria']
        Sassuolo = formazioni['Sassuolo']
        Spezia = formazioni['Spezia']
        Torino = formazioni['Torino']
        Udinese = formazioni['Udinese']
        Verona = formazioni['Verona']
        Lineups = {'ATALANTA':Atalanta,'BENEVENTO':Benevento,'BOLOGNA':Bologna,'CAGLIARI':Cagliari,'CROTONE':Crotone,'FIORENTINA':Fiorentina,'GENOA':Genoa,'INTER':Inter,'JUVENTUS':Juventus,'LAZIO':Lazio,'MILAN':Milan, 'NAPOLI':Napoli, 'PARMA':Parma,'ROMA':Roma,'SAMPDORIA':Sampdoria,'SASSUOLO':Sassuolo,'SPEZIA':Spezia,'TORINO':Torino,'UDINESE':Udinese,'VERONA':Verona}
    
    if(league=="Ligue1"):
        Metz = formazioni['Metz']
        Bordeaux = formazioni['Bordeaux']
        Lorient = formazioni['Lorient']
        Monaco = formazioni['Monaco']
        Brest = formazioni['Brest']
        Nizza = formazioni['Nice']
        Strasburgo = formazioni['Strasbourg']
        Nimes = formazioni['NimesOlympique']
        Nantes = formazioni['Nantes']
        Rennes = formazioni['Rennes']
        Lille = formazioni['Lille']
        Angers = formazioni['Angers']
        SaintEtienne = formazioni['St.Etienne']
        PSG = formazioni['ParisSaint-Germain']
        Marsiglia = formazioni['Marseille']
        Montpellier = formazioni['Montpellier']
        Reims = formazioni['Reims']
        Digione = formazioni['Dijon']
        Lione = formazioni['Lyon']
        Lens = formazioni['Lens']
       
        Lineups = {'METZ':Metz,'BORDEAUX':Bordeaux,'LORIENT':Lorient,'MONACO':Monaco,'BREST':Brest,'NIZZA':Nizza,'STRASBURGO':Strasburgo,'NIMES':Nimes,'NANTES':Nantes,'RENNES':Rennes,'LILLE':Lille,'ANGERS':Angers,'SAINT-ETIENNE':SaintEtienne,'PSG':PSG,'MARSIGLIA':Marsiglia,'MONTPELLIER':Montpellier,'REIMS':Reims,'DIGIONE':Digione,'LIONE':Lione,'LENS':Lens}
    
    return Lineups
    
#checking if the name is all together or split in name and surname
def FixName(row):
    if(row['Nome']==''):
        name = row['Cognome']
    else:
        name = row['Nome']+' '+row['Cognome']
    return name

def ShortName(row):
    if(len(row['Cognome'].split(' '))==2 and row['Nome']==''):
        name = row['Cognome'][0]+". "+row['Cognome'].split(' ')[1]
    else:
        name = ''
    return name

def GetPredFile(giornata,league,dataset,formazioni,quote):
    #dataset = pd.read_excel('Results_Giornata_'+str(giornata)+'_2020.xlsx')

    output = pd.DataFrame()
    
    #formazioni = pd.read_excel('rosegazzetta'+str(giornata)+'.xlsx')
    
    #Formazioni = {'ATALANTA':Atalanta,'BENEVENTO':Benevento,'BOLOGNA':Bologna,'CAGLIARI':Cagliari,'CROTONE':Crotone,'FIORENTINA':Fiorentina,'GENOA':Genoa,'INTER':Inter,'JUVENTUS':Juventus,'LAZIO':Lazio,'MILAN':Milan, 'NAPOLI':Napoli, 'PARMA':Parma,'ROMA':Roma,'SAMPDORIA':Sampdoria,'SASSUOLO':Sassuolo,'SPEZIA':Spezia,'TORINO':Torino,'UDINESE':Udinese,'VERONA':Verona}
    Formazioni = GetListLU(league,formazioni) #getting dictionary of lineups
    
    #quote = pd.read_excel('Snai_quotes_2020_8.xlsx')
    Casa = quote['HomeTeam'].str.upper()
    Trasferta = quote['AwayTeam'].str.upper()
    
    HomeMV = []
    
    #Giocatori = [' '.join(w for w in a.split() if w.isupper())  for a in dataset['Cognome']]

    #checking if the name is all together or split in name and surname    
    dataset['FullName'] = dataset.apply(FixName,axis=1)
    dataset['ShortName'] = dataset.apply(ShortName,axis=1) #add punctuation to extended surname..e.g. Rapahel Guerreiro -> R. Guerreiro
    
    from unidecode import unidecode
        
    for column in formazioni.columns[0:]:
        formazioni[column] = formazioni[column].apply(unidecode)
        formazioni[column] = formazioni[column].str.upper()
    
    #fixing few names which were too complicated to fix
    if(league=="Bundesliga"):
        formazioni['FCAugsburg'] = formazioni['FCAugsburg'].replace('IAGO','IAGO BORDUCHI')
        formazioni['FSVMainz05'] = formazioni['FSVMainz05'].replace('L. BARREIRO','L. BARREIRO MARTINS')
    if(league=="SerieA"):
        formazioni['Cagliari'] = formazioni['Cagliari'].replace('JOAO PEDRO','JOAO PEDRO GALVAO')
        formazioni['Spezia'] = formazioni['Spezia'].replace("N'ZOLA","M. N'ZOLA")
        formazioni['Crotone'] = formazioni['Crotone'].replace("SIMY","S. NWANKWO")
        formazioni['Verona'] = formazioni['Verona'].replace('E. SALCEDO','E. SALCEDO MORA')
        formazioni['Sassuolo'] = formazioni['Sassuolo'].replace('G. KYRIAKOPOULOS','G. KIRIAKOPOULOS')
        formazioni['Bologna'] = formazioni['Bologna'].replace('A. DA COSTA','ANGELO DA COSTA')
        formazioni['Crotone'] = formazioni['Crotone'].replace('P. MIGUEL PEREIRA','P. PEREIRA')
        formazioni['Juventus'] = formazioni['Juventus'].replace('A. MORATA','MORATA')
    if(league=="Ligue1"):
        formazioni['Brest'] = formazioni['Brest'].replace("H. MBOCK",'H. MANANGA MBOCK')
        formazioni['Metz'] = formazioni['Metz'].replace("A. LEYA ISEKA","A. LEYA")
        formazioni['Metz'] = formazioni['Metz'].replace("R. KOLO MUANI","R. MUANI")
        formazioni['St.Etienne'] = formazioni['St.Etienne'].replace("KOLO","T. KOLODZIEJCZAK")
        formazioni['St.Etienne'] = formazioni['St.Etienne'].replace("L. GOURNA-DOUATH","L. DOUATH")
        formazioni['Marseille'] = formazioni['Marseille'].replace("ALVARO","ALVARO GONZALEZ")
        formazioni['Lille'] = formazioni['Lille'].replace("R. MANDAVA","REINILDO")
        formazioni['Lyon'] = formazioni['Lyon'].replace("P. KADEWERE","T. KADEWERE")
        formazioni['Nice'] = formazioni['Nice'].replace("K. THURAM","K. THURAM-ULIE")
        formazioni['Nice'] = formazioni['Nice'].replace("YOUCEF ATAL","Y. ATTAL")
        formazioni['Bordeaux'] = formazioni['Bordeaux'].replace("UI-JO HWANG","HWANG UIJO")
        formazioni['Monaco'] = formazioni['Monaco'].replace("C. OLIVEIRA SILVA","CAIO HENRIQUE")
        formazioni['Montpellier'] = formazioni['Montpellier'].replace("IL-LOK YUN","YUN ILLOK")
        formazioni['Montpellier'] = formazioni['Montpellier'].replace("J. SAMBIA","S. SAMBIA")
        formazioni['Montpellier'] = formazioni['Montpellier'].replace("H. VITORINO","HILTON")
        formazioni['Dijon'] = formazioni['Dijon'].replace("N. MUZINGA","M. NGONDA")
        formazioni['Dijon'] = formazioni['Dijon'].replace("E. DINA EBIMBE","E. EBIMBE")
        formazioni['Dijon'] = formazioni['Dijon'].replace("P. CHEIKH DIOP","P. DIOP")
        formazioni['Lens'] = formazioni['Lens'].replace("A. KALIMUENDO MUINGA","A. KALIMUENDO")
        
    for squadra in Casa:
        print(squadra)
        #print(dataset[(dataset['Giocatore'].str.split(' ')[0].isin(Formazioni[squadra])) & (dataset['Squadra']=='LECCE')]['Prediction'])
        ngioc = 0
        list_pl_pred = [] #list of predicted mv
        for pl in Formazioni[squadra]:
            print(pl)
            if dataset[dataset['Squadra']==squadra]['FullName'].str.contains(pl).any():
                print('Player found WITH FULL NAME')
                list_pl_pred.append(dataset[(dataset['Squadra']==squadra) & (dataset['FullName']==pl)]['Prediction'].iloc[0])
                print(dataset[(dataset['Squadra']==squadra) & (dataset['FullName']==pl)]['Prediction'].iloc[0])
                ngioc +=1
            else:
                if len(pl.split('.'))==1:
                    if dataset[dataset['Squadra']==squadra]['Cognome'].str.contains(pl.split(' ')[1]).any():
                        print('Found with surname!')
                        subname = pl.split(' ')[1] #take only surname
                        list_pl_pred.append(dataset[(dataset['Squadra']==squadra) & (dataset['Cognome']==subname)]['Prediction'].iloc[0])
                        print(dataset[(dataset['Squadra']==squadra) & (dataset['Cognome']==subname)]['Prediction'].iloc[0])
                        ngioc += 1
                    else:
                        print('player not found!')
                else:
                    if dataset[dataset['Squadra']==squadra]['ShortName'].str.contains(pl).any():
                        list_pl_pred.append(dataset[(dataset['Squadra']==squadra) & (dataset['ShortName']==pl)]['Prediction'].iloc[0])
                        ngioc += 1
                        print('player found WITH SHORT NAME!')
                    else:
                        print('player not found!')
                    
        print('------->ngioc: ',ngioc)
        print("Mean: ",statistics.mean(list_pl_pred))

        HomeMV.append(statistics.mean(list_pl_pred))
    
    AwayMV = []
    
    for squadra in Trasferta:
        print(squadra)
        ngioc = 0
        list_pl_pred = [] #list of predicted mv
        for pl in Formazioni[squadra]:
            print(pl)
            if dataset[dataset['Squadra']==squadra]['FullName'].str.contains(pl).any():
                print('Player found')
                list_pl_pred.append(dataset[(dataset['Squadra']==squadra) & (dataset['FullName']==pl)]['Prediction'].iloc[0])
                print(dataset[(dataset['Squadra']==squadra) & (dataset['FullName']==pl)]['Prediction'].iloc[0])
                ngioc +=1
            else:
                if len(pl.split('.'))==1:
                    if dataset[dataset['Squadra']==squadra]['Cognome'].str.contains(pl.split(' ')[1]).any():
                        print('Found with surname!')
                        subname = pl.split(' ')[1] #take only surname
                        list_pl_pred.append(dataset[(dataset['Squadra']==squadra) & (dataset['Cognome']==subname)]['Prediction'].iloc[0])
                        print(dataset[(dataset['Squadra']==squadra) & (dataset['Cognome']==subname)]['Prediction'].iloc[0])
                        ngioc += 1
                    else:
                        print('player not found!')
                else:
                    if dataset[dataset['Squadra']==squadra]['ShortName'].str.contains(pl).any():
                        list_pl_pred.append(dataset[(dataset['Squadra']==squadra) & (dataset['ShortName']==pl)]['Prediction'].iloc[0])
                        ngioc += 1
                        print('player found!')
                    else:
                        print('player not found!')
                    
        print('------->ngioc: ',ngioc)
        print("Mean: ",statistics.mean(list_pl_pred))

        AwayMV.append(statistics.mean(list_pl_pred))
        
    output['HomeTeam'] = HomeMV
    output['AwayTeam'] = AwayMV
    
    #Adding xG
    df_xG = pd.read_excel(league+"/xG_tot_all_"+str(giornata)+".xlsx")
    df_xGA = pd.read_excel(league+"/xGA_tot_all_"+str(giornata)+".xlsx")
    
    Home_xG = []
    Home_xGA = []
    
    for squadra in Casa:
        Home_xG.append(df_xG[df_xG.Team.isin([squadra])].iloc[0]['Giornata '+str(giornata)])
        Home_xGA.append(df_xGA[df_xGA.Team.isin([squadra])].iloc[0]['Giornata '+str(giornata)])
    
    Away_xG = []
    Away_xGA = []
    
    for squadra in Trasferta:
        Away_xG.append(df_xG[df_xG.Team.isin([squadra])].iloc[0]['Giornata '+str(giornata)])
        Away_xGA.append(df_xGA[df_xGA.Team.isin([squadra])].iloc[0]['Giornata '+str(giornata)])

    output['HomexG'] = Home_xG
    output['AwayxG'] = Away_xG
    output['HomexGA'] = Home_xGA
    output['AwayxGA'] = Away_xGA
    output['HomeWin'] = quote['HomeWin']
    output['Draw'] = quote['Draw']
    output['AwayWin'] = quote['AwayWin']
    output['Casa'] = Casa
    output['Trasferta'] = Trasferta
    
    output.to_excel('Input_Scommessa_'+str(giornata)+'.xlsx')
    
    return output

def CreateCalendarInput(league,giornata,dataset):
    
    output = pd.DataFrame()
    output['HomeTeam'] = dataset['home']
    output['AwayTeam'] = dataset['away']
    
    output['Result'] = 0 #Setting all results to Draw
    output.loc[dataset['goals_home']>dataset['goals_away'],'Result']=1 #Setting all home wins to 1
    output.loc[dataset['goals_home']<dataset['goals_away'],'Result']=-1 #Setting all away wins to -1
    
    #Aggiungere over/under 2.5
    output['Over2.5'] = 0 #Setting all results to Under
    output.loc[dataset['goals_home']+dataset['goals_away']>2.5,'Over2.5']=1

    output['Giornata'] = dataset['Giornata']     
    output.to_excel(league+'/CalendarResults_until_round'+str(giornata)+'.xlsx')
    return output

def KNN(dataset,calendar,expgo,expgoAG,InScommessa):
    print("Using KNN)")
    
    hometeam = []
    awayteam = []
    result = []
    xGhome = []
    xGaway = []
    xGAhome = []
    xGAaway = []
    
    for index, row in calendar.iterrows():
        print(row['HomeTeam'])
        print(row['AwayTeam'])
        #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        hometeam.append(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        awayteam.append(dataset.loc[(dataset['Squadra']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        result.append(row['Result'])
    for index, row in calendar.iterrows():
        
        #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGhome.append(expgo.loc[(expgo['Team']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGaway.append(expgo.loc[(expgo['Team']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        
    for index, row in calendar.iterrows():
        #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGAhome.append(expgoAG.loc[(expgoAG['Team']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGAaway.append(expgoAG.loc[(expgoAG['Team']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        
    inML = pd.DataFrame()
    inML['HomeTeam'] = 0
    inML['HomeTeam'] = hometeam
    inML['AwayTeam'] = awayteam
    inML['HomexG'] = xGhome
    inML['AwayxG'] = xGaway
    inML['HomexGA'] = xGAhome
    inML['AwayxGA'] = xGAaway
    inML['Result'] = result
    
    inML = inML.dropna()

    X = inML.iloc[:, 0:6].values
    y = inML.iloc[:, -1].values

    from sklearn.model_selection import train_test_split #model selection
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
    
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)
    
    #PROVO ALTRI MODELLI
    from sklearn.metrics import accuracy_score, log_loss
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC, LinearSVC, NuSVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="rbf",random_state=0, probability=True),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        AdaBoostClassifier(),
        GradientBoostingClassifier()
        ]
    for classifier in classifiers:
        model = classifier.fit(X_train, y_train)
        print(classifier)
        print("model score: %.3f" % model.score(X_test, y_test))
     
    #TRY TO FIND BEST PARAMETERS FOR EACH MODEL
    #1) KNEIGHBORS because it gives best results
    from sklearn.model_selection import GridSearchCV
    p = [1, 2, 3, 4, 5, 6]
    leaf_size = [5, 15, 20, 30, 35, 50, 80]
    n_neighbors = [1,2, 3, 4, 5, 7, 10]
    weights = ['uniform', 'distance']
    param_grid = dict(p = p, leaf_size = leaf_size,  
                  n_neighbors = n_neighbors, 
                 weights = weights)
    kn = KNeighborsClassifier(3)
    grid_search = GridSearchCV(estimator=kn, param_grid=param_grid)
    best_model = grid_search.fit(X_train, y_train)
    print(round(best_model.score(X_test, y_test),2))
    print(best_model.best_params_)
    
    #best_model = KNeighborsClassifier(3).fit(X_train, y_train)
    #print(best_model.score(X_test,y_test),2)
    #TEST TEST TEST
    from sklearn.metrics import classification_report
    y_pred_best = best_model.predict(X_test)
    print(classification_report(y_test, y_pred_best))
    
    from sklearn.metrics import confusion_matrix #it's a function..not a class!
    cm = confusion_matrix(y_test,y_pred_best)    

    kellyTestxG = InScommessa.iloc[:, 0:6].values

    kellyTestxG = sc_X.transform(kellyTestxG)
    kellyPredictxG = best_model.predict(kellyTestxG)
    probabilityxG = best_model.predict_proba(kellyTestxG)

    HomeQuotes = InScommessa['HomeWin']/1000
    DrawQuotes = InScommessa['Draw']/1000
    AwayQuotes = InScommessa['AwayWin']/1000
    Casa = InScommessa['Casa']
    Trasferta = InScommessa['Trasferta']
    CasaxG = InScommessa['HomexG']
    TrasfertaxG = InScommessa['AwayxG']

    budget = 10
    guadagno = 0
    perdita = 0
    diff = 0
    spesa = 0
    
    for i in range(0,len(kellyPredictxG)): 
        print("#####")
        print("{0} vs {1}".format(Casa[i],Trasferta[i]))
        print("HOME WIN")
        d = DrawQuotes[i]-1
        b = HomeQuotes[i]-1
        p = probabilityxG[i][2]
        q = 1-p
        kFact = ((b*p-q)/b)/2
        #dnb = kFact/d
        print(kFact)
        #print("Draw No Bet 1: {}".format(dnb))
        print("DRAW")
        b = DrawQuotes[i]-1
        p = probabilityxG[i][1]
        q = 1-p
        kFact = ((b*p-q)/b)/2
        print(kFact)
        print("AWAY WIN")
        d = DrawQuotes[i]-1
        b = AwayQuotes[i]-1
        p = probabilityxG[i][0]
        q = 1-p
        kFact = ((b*p-q)/b)/2
        #dnb = kFact/d
        #print("Draw No Bet 2: {}".format(dnb))
        print(kFact)
        
    return inML,X,y,cm,kellyTestxG,kellyPredictxG,probabilityxG
            

def RandomForest(dataset,calendar,expgo,expgoAG,InScommessa):
    print("Using KNN)")
    
    hometeam = []
    awayteam = []
    result = []
    xGhome = []
    xGaway = []
    xGAhome = []
    xGAaway = []
    
    for index, row in calendar.iterrows():
        print(row['HomeTeam'])
        print(row['AwayTeam'])
        #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        hometeam.append(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        awayteam.append(dataset.loc[(dataset['Squadra']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        result.append(row['Result'])
    for index, row in calendar.iterrows():
        
        #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGhome.append(expgo.loc[(expgo['Team']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGaway.append(expgo.loc[(expgo['Team']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        
    for index, row in calendar.iterrows():
        #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGAhome.append(expgoAG.loc[(expgoAG['Team']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        xGAaway.append(expgoAG.loc[(expgoAG['Team']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
        
    inML = pd.DataFrame()
    inML['HomeTeam'] = 0
    inML['HomeTeam'] = hometeam
    inML['AwayTeam'] = awayteam
    inML['HomexG'] = xGhome
    inML['AwayxG'] = xGaway
    inML['HomexGA'] = xGAhome
    inML['AwayxGA'] = xGAaway
    inML['Result'] = result
    
    inML = inML.dropna()

    X = inML.iloc[:, 0:6].values
    y = inML.iloc[:, -1].values

    from sklearn.model_selection import train_test_split #model selection
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
    
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)
    
    #PROVO ALTRI MODELLI
    from sklearn.metrics import accuracy_score, log_loss
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC, LinearSVC, NuSVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="rbf",random_state=0, probability=True),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        AdaBoostClassifier(),
        GradientBoostingClassifier()
        ]
    for classifier in classifiers:
        model = classifier.fit(X_train, y_train)
        print(classifier)
        print("model score: %.3f" % model.score(X_test, y_test))
     
    #TRY TO FIND BEST PARAMETERS FOR EACH MODEL
    #1) RANDOM FOREST because it gives best results
    from sklearn.model_selection import GridSearchCV
    n_estimators = [1 , 5, 10, 15, 20]
    max_depth = [2 , 5, 8, 15, 25, 30]
    min_samples_split = [2, 5, 10, 15]
    min_samples_leaf = [1, 2, 5, 10]
    param_grid = dict(n_estimators = n_estimators, max_depth = max_depth,  
                  min_samples_split = min_samples_split, 
                 min_samples_leaf = min_samples_leaf)
    rf = RandomForestClassifier()
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid)
    best_model = grid_search.fit(X_train, y_train)
    print(round(best_model.score(X_test, y_test),2))
    print(best_model.best_params_)
    
    from sklearn.metrics import classification_report
    y_pred_best = best_model.predict(X_test)
    print(classification_report(y_test, y_pred_best))
    
    from sklearn.metrics import confusion_matrix #it's a function..not a class!
    cm = confusion_matrix(y_test,y_pred_best)    

    kellyTestxG = InScommessa.iloc[:, 0:6].values

    kellyTestxG = sc_X.transform(kellyTestxG)
    kellyPredictxG = best_model.predict(kellyTestxG)
    probabilityxG = best_model.predict_proba(kellyTestxG)

    HomeQuotes = InScommessa['HomeWin']/1000
    DrawQuotes = InScommessa['Draw']/1000
    AwayQuotes = InScommessa['AwayWin']/1000
    Casa = InScommessa['Casa']
    Trasferta = InScommessa['Trasferta']
    CasaxG = InScommessa['HomexG']
    TrasfertaxG = InScommessa['AwayxG']

    budget = 10
    guadagno = 0
    perdita = 0
    diff = 0
    spesa = 0
    
    for i in range(0,len(kellyPredictxG)): 
        print("#####")
        print("{0} vs {1}".format(Casa[i],Trasferta[i]))
        print("HOME WIN")
        d = DrawQuotes[i]-1
        b = HomeQuotes[i]-1
        p = probabilityxG[i][2]
        q = 1-p
        kFact = ((b*p-q)/b)/2
        #dnb = kFact/d
        print(kFact)
        #print("Draw No Bet 1: {}".format(dnb))
        print("DRAW")
        b = DrawQuotes[i]-1
        p = probabilityxG[i][1]
        q = 1-p
        kFact = ((b*p-q)/b)/2
        print(kFact)
        print("AWAY WIN")
        d = DrawQuotes[i]-1
        b = AwayQuotes[i]-1
        p = probabilityxG[i][0]
        q = 1-p
        kFact = ((b*p-q)/b)/2
        #dnb = kFact/d
        #print("Draw No Bet 2: {}".format(dnb))
        print(kFact)
        
    return inML,X,y,cm,kellyTestxG,kellyPredictxG,probabilityxG        
        
        
        
        
        