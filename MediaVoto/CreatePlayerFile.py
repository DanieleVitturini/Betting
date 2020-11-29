#Crea un file con la Fantamedia/MediaVoto/Costo di ogni giocatore per partita
def ChangeColumnName(df,name):
    df = df.rename(columns={"Voto Pagella": name})
    return df
def ImportData(giornata):
    dataset = pd.read_excel('../Voti/2020/quotazioni_gazzetta_'+giornata+'.xls')
    dataset = dataset.replace('-',0)
    dataset = dataset.replace(np.nan, 0)
    return dataset
    
# Importing the libraries
import pandas as pd
import numpy as np

# Importing the dataset
dataset = ImportData("1")
dataset = ChangeColumnName(dataset,"Giornata 1")

df = ImportData("2")
df = ChangeColumnName(df,"Giornata 2")

output = pd.merge(dataset[['Cod.','Giocatore','Squadra','Ruolo','Giornata 1']],df[['Cod.','Giocatore','Squadra','Ruolo','Giornata 2']],on=['Cod.','Giocatore','Ruolo','Squadra'],how='outer')

#Giornate = ['03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
Giornate = np.arange(3,9) #le prime due sono già prese e merged. NB:metti secondo valore per giornata che vuoi predidiscere

for giorn in Giornate:
    newdata = ImportData(str(giorn))
    newdata = ChangeColumnName(newdata,"Giornata "+str(giorn))
    output = pd.merge(output,newdata[['Cod.','Giocatore','Ruolo','Squadra','Giornata '+str(giorn)]],on=['Cod.','Giocatore','Ruolo','Squadra'],how='outer')

### CHANGE HERE Giornata -> to the last before the prediction (ALL TRUE DATA HERE)
mv_anno = output.loc[:,'Giornata 1':'Giornata {0}'.format(Giornate[-1])].replace(0,np.NaN).mean(axis=1,numeric_only=True).replace(np.NaN,0)
output['MediaVotoTot'] = mv_anno
output = output.replace(np.NaN,0)
#output = output.drop_duplicates(subset = 'Giocatore', keep = 'last')
output.to_excel('MediaVoto_giocatori.xlsx')
