# Create ML input
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
    
import pandas as pd
import numpy as np

dPlayers = pd.read_excel('MediaVoto_giocatori.xlsx')
dTeam = pd.read_excel('FantaMedia_Squadre.xlsx')
dCalendar = pd.read_excel('../CalendarSerieA.xlsx')
dPlayers = dPlayers.replace(np.NaN,0)

output = pd.DataFrame()

#Giornate = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
Giornate = np.arange(5,15)
Squadre = ['Atalanta','Benevento','Bologna','Cagliari','Crotone','Fiorentina','Genoa','Inter','Juventus','Lazio','Milan','Napoli','Parma','Roma','Sampdoria','Sassuolo','Spezia','Torino','Udinese','Verona']
Squadre = [x.upper() for x in Squadre]

for giorn in Giornate:
    for club in Squadre:
        output = CreateInputML(club,giorn,output,dPlayers,dTeam,dCalendar)

output.to_excel('ML_MediaVoto_input.xlsx')