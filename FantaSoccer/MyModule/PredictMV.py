#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:20:39 2020

@author: peter
"""

import pandas as pd
import numpy as np

def ChangeColumnName(df,name):
    df = df.rename(columns={"Voto FS": name})
    return df
def ImportData(giornata,league):
    if league=="SerieA":
        dataset = pd.read_excel('../Voti/SerieA/Voti_'+giornata+'a_SerieA.xlsx')
    if league=="PremierLeague":
        dataset = pd.read_excel('../Voti/PremierLeague/Voti_'+giornata+'a_SerieC.xlsx')
    if league=="Bundesliga":
        dataset = pd.read_excel('../Voti/Bundesliga/Voti_'+giornata+'a_SerieE.xlsx')
    if league=="Ligue1":
        dataset = pd.read_excel('../Voti/Ligue1/Voti_'+giornata+'a_SerieF.xlsx')
        
    dataset = dataset.replace('-',0)
    dataset = dataset.replace(np.nan, 0)
    return dataset

def CreatePlayerFile(giornata,league):
    dataset = ImportData("1",league)
    dataset = ChangeColumnName(dataset,"Giornata 1")
    
    df = ImportData("2",league)
    df = ChangeColumnName(df,"Giornata 2")
    print(dataset.columns)
    output = pd.merge(dataset[['CodiceCalciatore','Cognome','Nome','Squadra','Ruolo','Giornata 1']],df[['CodiceCalciatore','Cognome','Nome','Squadra','Ruolo','Giornata 2']],on=['CodiceCalciatore','Cognome','Nome','Ruolo','Squadra'],how='outer')
    
    #Giornate = ['03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
    Giornate = np.arange(3,giornata) #le prime due sono già prese e merged
    output = output.replace('SV',0)
    output["Giornata 1"] = pd.to_numeric(output["Giornata 1"], downcast="float")
    output["Giornata 2"] = pd.to_numeric(output["Giornata 2"], downcast="float")
    
    for giorn in Giornate:
        newdata = ImportData(str(giorn),league)
        newdata = ChangeColumnName(newdata,"Giornata "+str(giorn))
        output = pd.merge(output,newdata[['CodiceCalciatore','Cognome','Nome','Ruolo','Squadra','Giornata '+str(giorn)]],on=['CodiceCalciatore','Cognome','Nome','Ruolo','Squadra'],how='outer')
        output = output.replace(np.NaN,0)
        output = output.replace('SV',0)
        output["Giornata "+str(giorn)] = pd.to_numeric(output["Giornata "+str(giorn)], downcast="float")
        
    ### CHANGE HERE Giornata -> to the last before the prediction (ALL TRUE DATA HERE)
    mv_anno = output.loc[:,'Giornata 1':'Giornata {0}'.format(Giornate[-1])].replace(0,np.NaN).mean(axis=1,numeric_only=True).replace(np.NaN,0)
    output['MediaVotoTot'] = mv_anno
    
    #it fixes an issue with UTF encoding
    for col in output.columns:
        if output[col].dtype==object:
            output[col]=output[col].apply(lambda x: np.nan if x==np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))
    
    
    #it merges the data of players which switched team (e.g. Bonazzoli)
    #output = output.groupby('CodiceCalciatore').max().reset_index()
    output['Squadra'] = output['Squadra'].str.upper()
    output = output[output['Ruolo']!='0']
    output = output[output['MediaVotoTot']!=0] #dropping players with MV tot=0 and trainers
    
    output['Nome'] = output['Nome'].replace('0','')
    
    output.to_excel(league+"/MediaVoto_giocatori_"+str(giornata)+".xls")
    return output

def CreateTeamFile(giornata,league,dataset):
    
    #dataset = pd.read_excel('MediaVoto_giocatori.xls')

    output = pd.DataFrame()

    Giornate = np.arange(1,giornata) #mettere la giornata che si vuole predire perchè il range arriva fino a n-1
    for giorn in Giornate:
        fm = dataset[dataset['Giornata '+str(giorn)]!=0].groupby(['Squadra'])['Giornata '+str(giorn)].mean()
        output['Giornata '+str(giorn)] = pd.Series(fm)
    tot = output.mean(axis=1)
    output['Total average '] = pd.Series(tot)
    
    output = output.replace(np.nan,6)
    output.reset_index(level=0, inplace=True) #the team column is set to index before, converting it in a real column
    output.to_excel(league+"/MediaVoto_squadre_"+str(giornata)+".xls")
    return output


def CreateInputPred(index,team_name,giorn,output,dPlayers,dTeam,dCalendar):
    print(giorn)
    print(index)
    print(team_name)
    new_data = pd.DataFrame()
    Squadra = pd.Series(dPlayers[(dPlayers['Squadra']==team_name)]['Squadra'])
    Ruolo = pd.Series(dPlayers[(dPlayers['Squadra']==team_name)]['Ruolo'])
    MV = pd.Series(dPlayers[(dPlayers['Squadra']==team_name)]['MediaVotoTot'])
    LastMV = pd.Series(dPlayers[['Giornata '+str(index-1),'Giornata '+str(index-2),'Giornata '+str(index-3),'Giornata '+str(index-4),'Giornata '+str(index-5)]].mean(axis=1))
    MediaTeam = pd.Series(dTeam[['Giornata '+str(index-1),'Giornata '+str(index-2),'Giornata '+str(index-3),'Giornata '+str(index-4),'Giornata '+str(index-5)]].mean(axis=1))     
    dTeam['TeamMV'] = pd.Series(MediaTeam)
    TeamMV = float(dTeam[dTeam['Squadra']==team_name]['TeamMV'])
    print(float(dTeam[dTeam['Squadra']==team_name]['TeamMV']))
    #print(dCalendar[team_name+'Opponent'][index])
    OppMV = float(dTeam[dTeam['Squadra']==str(dCalendar[team_name+'Opponent'][index])]['TeamMV'])

    new_data['Squadra'] = pd.Series(Squadra)
    new_data['Ruolo'] = pd.Series(Ruolo) 
    new_data['MVTot'] = pd.Series(MV) 
    new_data['LastMV'] = pd.Series(LastMV)
    new_data['TeamMV'] = TeamMV  
    new_data['OppMV'] = OppMV
    new_data['Opponent'] = dCalendar[team_name+'Opponent'][index]
    new_data['IsHome'] = dCalendar[team_name+'IsHome'][index]
      
    new_data = pd.merge(new_data,dPlayers[['CodiceCalciatore']],left_index=True, right_index=True)
    #print(new_data)  

    frames = [output,new_data]
    final = pd.concat(frames)
    final = final.reset_index(drop=True)
    
    return final

def CreatePredictionFile(giornata,league,dPlayers,dTeam,dCalendar):
    
    output = pd.DataFrame()

    if(league=="SerieA"):
        Squadre = ['Atalanta','Benevento','Bologna','Cagliari','Crotone','Fiorentina','Genoa','Inter','Juventus','Lazio','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="PremierLeague"):
        Squadre = ['Arsenal','Aston Villa','Brighton Hove','Burnley','Chelsea','Crystal Palace','Everton','Fulham','Leeds United','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle','Sheffield United','Southampton','Tottenham','West Bromwich','West Ham','Wolverhampton']
    if(league=="Bundesliga"):
        Squadre = ['Arminia Bielefeld','Augsburg','Bayern Monaco','Borussia Dortmund','Borussia MGladbach','Colonia','Eintracht Francoforte','Friburgo','Hertha','Hoffenheim','Leverkusen','Mainz','RB Lipsia','Schalke 04','Stoccarda','Union Berlino','Werder Brema','Wolfsburg']
    if(league=="Ligue1"):
        Squadre = ['Angers','Bordeaux','Brest','Digione','Lens','Lille','Lorient','Lione','Marsiglia','Metz','Monaco','Montpellier','Nantes','Nizza','Nimes','PSG','Reims','Rennes','Saint-Etienne','Strasburgo']
   
    Squadre = [x.upper() for x in Squadre]
    
    for club in Squadre:#set the number to n-1 where n is the round you want to predict (need to be changed)
            output = CreateInputPred(giornata-1,club,str(giornata-1),output,dPlayers,dTeam,dCalendar) #SET THE NUMBER TO THE LAST GIORNATA PLAYED
    
    output.to_excel(league+'/ML_MediaVoto_prediction'+str(giornata)+'.xlsx')
    return output

def CreateInputML(team_name,giorn,output,dPlayers,dTeam,dCalendar):
    print(giorn)
    print(team_name)
    new_data = pd.DataFrame()
    Squadra = pd.Series(dPlayers[(dPlayers['Giornata '+str(giorn)]!=0) & (dPlayers['Squadra']==team_name)]['Squadra'])
    Ruolo = pd.Series(dPlayers[(dPlayers['Giornata '+str(giorn)]!=0) & (dPlayers['Squadra']==team_name)]['Ruolo'])
    MV = pd.Series(dPlayers[(dPlayers['Giornata '+str(giorn)]!=0) & (dPlayers['Squadra']==team_name)]['MediaVotoTot'])
    
    final = pd.DataFrame()
    if(len(Squadra)==0):
        return output
    LastMV = pd.Series(dPlayers[['Giornata '+str(giorn),'Giornata '+str(giorn-1),'Giornata '+str(giorn-2),'Giornata '+str(giorn-3),'Giornata '+str(giorn-4)]].mean(axis=1))

    MediaTeam = pd.Series(dTeam[['Giornata '+str(giorn),'Giornata '+str(giorn-1),'Giornata '+str(giorn-2),'Giornata '+str(giorn-3),'Giornata '+str(giorn-4)]].mean(axis=1))     
    dTeam['TeamMV'] = pd.Series(MediaTeam)
    TeamMV = float(dTeam[dTeam['Squadra']==team_name]['TeamMV'])
    OppMV = float(dTeam[dTeam['Squadra']==str(dCalendar[team_name+'Opponent'][giorn])]['TeamMV'])
    new_data['Squadra'] = pd.Series(Squadra)
    new_data['Ruolo'] = pd.Series(Ruolo) 
    new_data['MVTot'] = pd.Series(MV) 
    new_data['LastMV'] = pd.Series(LastMV) 
    new_data['TeamMV'] = TeamMV  
    new_data['OppMV'] = OppMV
    new_data['Opponent'] = dCalendar[team_name+'Opponent'][giorn-1]
    new_data['IsHome'] = dCalendar[team_name+'IsHome'][giorn-1]
          
    new_data = pd.merge(new_data,dPlayers[['Giornata '+str(giorn)]],left_index=True, right_index=True)
    print(new_data)  
    new_data = new_data.rename(columns={"Giornata "+str(giorn): 'MediaVoto'})

    frames = [output,new_data]
    final = pd.concat(frames)
    final = final.reset_index(drop=True)
    
    return final

def GetMLInput(giornata,league,dPlayers,dTeam,dCalendar):

    dPlayers = dPlayers.replace(np.NaN,0)
    
    output = pd.DataFrame()
    
    #Giornate = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
    Giornate = np.arange(5,giornata)
    if(league=="SerieA"):
        Squadre = ['Atalanta','Benevento','Bologna','Cagliari','Crotone','Fiorentina','Genoa','Inter','Juventus','Lazio','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
    if(league=="PremierLeague"):
        Squadre = ['Arsenal','Aston Villa','Brighton Hove','Burnley','Chelsea','Crystal Palace','Everton','Fulham','Leeds United','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle','Sheffield United','Southampton','Tottenham','West Bromwich','West Ham','Wolverhampton']
    if(league=="Bundesliga"):
        Squadre = ['Arminia Bielefeld','Augsburg','Bayern Monaco','Borussia Dortmund','Borussia MGladbach','Colonia','Eintracht Francoforte','Friburgo','Hertha','Hoffenheim','Leverkusen','Mainz','RB Lipsia','Schalke 04','Stoccarda','Union Berlino','Werder Brema','Wolfsburg']
    if(league=="Ligue1"):
        Squadre = ['Angers','Bordeaux','Brest','Digione','Lens','Lille','Lorient','Lione','Marsiglia','Metz','Monaco','Montpellier','Nantes','Nizza','Nimes','PSG','Reims','Rennes','Saint-Etienne','Strasburgo']

    Squadre = [x.upper() for x in Squadre]
    
    for giorn in Giornate:
        for club in Squadre:
            output = CreateInputML(club,giorn,output,dPlayers,dTeam,dCalendar)
    
    output.to_excel(league+'/ML_MediaVoto_input_'+str(giornata)+'.xlsx')
    return output

def CreateCategory(dataset,category_name):
    from sklearn.preprocessing import LabelEncoder
    labelencoder_X = LabelEncoder()
    dataset[category_name] = labelencoder_X.fit_transform(dataset[category_name])

    from sklearn.preprocessing import OneHotEncoder
    city_ohe = OneHotEncoder()
    city_feature_arr = city_ohe.fit_transform(dataset[[category_name]]).toarray()
    city_feature_arr = pd.DataFrame(city_feature_arr)
    city_feature_arr = city_feature_arr.iloc[:,:-1] #eliminare la dummy variable
    return city_feature_arr
def CreateDataset(dataset):
    Squadra = CreateCategory(dataset,'Squadra')
    Ruolo = CreateCategory(dataset,'Ruolo')
    Opponent = CreateCategory(dataset,'Opponent')
    ML_input = pd.merge(Squadra,Opponent,left_index=True,right_index=True)
    ML_input = pd.merge(ML_input,Ruolo,left_index=True,right_index=True)
    ML_input['MVTot'] = dataset['MVTot']
    ML_input['LastMV'] = dataset['LastMV']
    ML_input['TeamMV'] = dataset['TeamMV']
    ML_input['OppMV'] = dataset['OppMV']
    ML_input['IsHome'] = dataset['IsHome']
    return ML_input

def ML_regress_FS(giornata,league,dataset,prediction,dPlayers):
    
    #prediction = prediction[prediction['Ruolo']!='0']
    prediction = prediction.dropna()
    
    #X = dataset.iloc[:, 1:3].values
    y = dataset.iloc[:, 8].values
    
    X = CreateDataset(dataset)
        
    Pred = CreateDataset(prediction)
    

    Pred = Pred.dropna()
    
    #Tante complicazioni inutili, servirebbe passare a una nuova versione di python per usare ColumnTransformer
    
    #Splitting the dataset into training and test dataset
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    
    #Fitting multiple linear regression to the training set
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train,y_train)
    #Predicting the test results
    
    NewPred = regressor.predict(Pred)
    prediction['Prediction'] = pd.Series(NewPred)
    
    Output = dPlayers[['CodiceCalciatore','Cognome','Nome','Ruolo','Squadra']]
    Output = pd.merge(Output,prediction[['CodiceCalciatore','Prediction']],on='CodiceCalciatore')
    Output = Output.drop_duplicates(subset = ['Cognome','Nome','Squadra'], keep = 'last')
    Output['Cognome'] = Output['Cognome'].str.upper()
     
    Output.to_excel(league+'/Results_Giornata_'+str(giornata)+'_2020.xlsx')
    return Output


