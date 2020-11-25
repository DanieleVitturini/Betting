#Create file for prediction
def CreateInputML(index,team_name,giorn,output,dPlayers,dTeam,dCalendar):
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
    OppMV = float(dTeam[dTeam['Squadra']==str(dCalendar[team_name+'Opponent'][index])]['TeamMV'])

    new_data['Squadra'] = pd.Series(Squadra)
    new_data['Ruolo'] = pd.Series(Ruolo) 
    new_data['MVTot'] = pd.Series(MV) 
    new_data['LastMV'] = pd.Series(LastMV)
    new_data['TeamMV'] = TeamMV  
    new_data['OppMV'] = OppMV
    new_data['Opponent'] = dCalendar[team_name+'Opponent'][index]
    new_data['IsHome'] = dCalendar[team_name+'IsHome'][index]
      
    new_data = pd.merge(new_data,dPlayers[['Cod.']],left_index=True, right_index=True)
    print(new_data)  

    frames = [output,new_data]
    final = pd.concat(frames)
    final = final.reset_index(drop=True)
    
    return final
    
import pandas as pd    

dPlayers = pd.read_excel('MediaVoto_giocatori.xlsx')
dTeam = pd.read_excel('FantaMedia_Squadre.xlsx')
dCalendar = pd.read_excel('../Calendar.xlsx')
output = pd.DataFrame()

#Giornate = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
Squadre = ['Atalanta','Benevento','Bologna','Cagliari','Crotone','Fiorentina','Genoa','Inter','Juventus','Lazio','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
Squadre = [x.upper() for x in Squadre]

for club in Squadre:
        output = CreateInputML(7,club,'7',output,dPlayers,dTeam,dCalendar) #SET THE NUMBER TO THE LAST GIORNATA PLAYED

output.to_excel('ML_MediaVoto_prediction.xlsx')

