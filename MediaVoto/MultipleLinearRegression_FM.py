#Multiple linear regression -> FantaMedia
#import libraries
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
    
import pandas as pd
import matplotlib.pyplot as plt
#import dataset
dataset = pd.read_excel("ML_MediaVoto_input.xlsx")
prediction = pd.read_excel('ML_MediaVoto_prediction.xlsx')

#X = dataset.iloc[:, 1:3].values
y = dataset.iloc[:, 9].values
df_y = pd.DataFrame(y)

X = CreateDataset(dataset)
    
Pred = CreateDataset(prediction)

#Tante complicazioni inutili, servirebbe passare a una nuova versione di python per usare ColumnTransformer

#Splitting the dataset into training and test dataset
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#Fitting multiple linear regression to the training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train,y_train)
#Predicting the test results
y_pred = regressor.predict(X_test)

NewPred = regressor.predict(Pred)
prediction['Prediction'] = pd.Series(NewPred)

dPlayers = pd.read_excel('MediaVoto_giocatori.xlsx')
Output = dPlayers[['Cod.','Giocatore','Ruolo','Squadra']]
Output = pd.merge(Output,prediction[['Cod.','Prediction']],on='Cod.')
Output = Output.drop_duplicates(subset = 'Giocatore', keep = 'last')
Output.to_excel('Results_Giornata_8_2020.xlsx')

diff = y_test-y_pred
plt.hist(diff,bins=100)

plt.scatter(y_test, y_pred,alpha=0.5)
plt.xlabel('y_test')
plt.ylabel('y_pred')
plt.show()

plt.scatter(y_test, diff,alpha=0.5)
plt.xlabel('y_test')
plt.ylabel('diff')
plt.show()