# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_excel('FantaMedia_Squadre.xlsx')
calendar = pd.read_excel('Calendar.xlsx')

hometeam = []
awayteam = []
result = []
for index, row in calendar.iterrows():
    #print(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
    hometeam.append(dataset.loc[(dataset['Squadra']==row['HomeTeam'])]['Giornata '+str(row['Giornata'])].values[0])
    awayteam.append(dataset.loc[(dataset['Squadra']==row['AwayTeam'])]['Giornata '+str(row['Giornata'])].values[0])
    
inML = pd.DataFrame()
inML['HomeTeam'] = 0
inML['HomeTeam'] = hometeam
inML['AwayTeam'] = awayteam
inML['B365H'] = calendar['B365H']
inML['B365D'] = calendar['B365D']
inML['B365A'] = calendar['B365A']
inML['Result'] = calendar['Result']

#Logistic regression
inML = inML.dropna()

X = inML.iloc[:, 0:2].values
y = inML.iloc[:, -1].values

from sklearn.model_selection import train_test_split #model selection
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

#Fitting the classifier to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel='rbf', random_state=0, probability=True)
classifier.fit(X_train,y_train)

#Predicting test results
y_pred = classifier.predict(X_test)

#Making the confusion matrix
from sklearn.metrics import confusion_matrix #it's a function..not a class!
cm = confusion_matrix(y_test,y_pred)

#Probability
results = classifier.predict_proba(X_test)

###EVALUATING QUOTES WITH KELLY FACTOR ###
InScommessa = pd.read_excel('Input_Scommessa_8.xlsx')
kellyTest = InScommessa.iloc[:, 1:3].values

kellyTest = sc_X.transform(kellyTest)
kellyPredict = classifier.predict(kellyTest)
probability = classifier.predict_proba(kellyTest)

HomeQuotes = InScommessa['HomeWin']
DrawQuotes = InScommessa['Draw']
AwayQuotes = InScommessa['AwayWin']
Casa = InScommessa['Casa']
Trasferta = InScommessa['Trasferta']

budget = 10
guadagno = 0
perdita = 0
diff = 0
spesa = 0

for i in range(0,len(kellyPredict)): 
    print("#####")
    print("{0} vs {1}".format(Casa[i],Trasferta[i]))
    print("HOME WIN")
    b = HomeQuotes[i]-1
    p = probability[i][2]
    q = 1-p
    kFact = ((b*p-q)/b)/2
    print(kFact)
    print("DRAW")
    b = DrawQuotes[i]-1
    p = probability[i][1]
    q = 1-p
    kFact = ((b*p-q)/b)/2
    print(kFact)
    print("AWAY WIN")
    b = HomeQuotes[i]-1
    p = probability[i][0]
    q = 1-p
    kFact = ((b*p-q)/b)/2
    print(kFact)

budget = 10
guadagno = 0
perdita = 0
diff = 0
spesa = 0

for i in range(0,len(kellyPredict)): 
    print("#####")
    print("{0} vs {1}".format(Casa[i],Trasferta[i]))
    print("HOME WIN")
    b = HomeQuotes[i]-1
    p = probability[i][2]
    q = 1-p
    kFact = ((b*p-q)/b)
    print(kFact)
    print("DRAW")
    b = DrawQuotes[i]-1
    p = probability[i][1]
    q = 1-p
    kFact = ((b*p-q)/b)
    print(kFact)
    print("AWAY WIN")
    b = HomeQuotes[i]-1
    p = probability[i][0]
    q = 1-p
    kFact = ((b*p-q)/b)
    print(kFact)
               
"""testresults = [1,-1,-1,-1,1,-1,0,-1,1]
quotes = [7.5,3.5,2.55,5,2.37,13,2.62,1.72,4.1]
Verona Juve 7.5,4,1.5,6.75
Torino Samp 2.15,3.3,3.5
Spal Sass 2.7,3.4,2.55
Roma Bologna 1.61,4.33,5
Genoa Cagl 2.37,3.5,2.9
Napoli Lecce 1.2,6.5,13
Brescia Udinese 2.7,3.4,2.62
Parma Lazio 4.5,4,1.72
Inter Milan 1.95,3.4,4.1"""



for i in range(0,len(kellyPredict)): 
    kFact=0    
    if kellyPredict[i]==1:
        print("#####")
        b = quotes[i]-1
        print(b)
        p = probability[i][2]
        print(p)
        q = 1-p
        kFact = ((b*p-q)/b)/2
        print(kFact)
    if kellyPredict[i]==-1:
        print("#####")
        b = quotes[i]-1
        print(b)
        p = probability[i][0]
        print(p)
        q = 1-p
        kFact = (b*p-q)/b
        print(kFact)
    if kFact>0:
        puntata = budget*kFact
        spesa = spesa+puntata
        print("Puntata: {0}".format(puntata))
        if kellyPredict[i]==testresults[i]:
            print("WON!")
            guadagno = puntata*(1+b) 
            diff = diff+guadagno
        else:
            print("LOST!")
            perdita = puntata
            diff = diff-perdita
    
    print("Guadagno: {0}".format(guadagno))
    print("Perdita: {0}".format(perdita))
    print("Diff: {0}".format(diff))
    print("Spesa: {0}".format(spesa))
    
budget = 100

for i in range(0,len(kellyPredict)): 
    kFact=0    
    if kellyPredict[i]==1:
        print("#####")
        b = testdata['B365H'].iloc[i]-1
        print(b)
        p = probability[i][2]
        print(p)
        q = 1-p
        kFact = ((b*p-q)/b)/2
        print(kFact)
    if kellyPredict[i]==-1:
        print("#####")
        b = testdata['B365H'].iloc[i]-1
        print(b)
        p = probability[i][0]
        print(p)
        q = 1-p
        kFact = (b*p-q)/b
        print(kFact)
    if kFact>0:
        puntata = budget*kFact
        if kellyPredict[i]==testdata['Result'].iloc[i]:
            print("WON!")
            guadagno = puntata*b
            budget = budget+guadagno
        else:
            print("LOST!")
            perdita = puntata
            budget = budget-perdita
    
    print("Budget: {0}".format(budget))
    
    
#Test 23esima giornata
casa = [6.42,5.69,5.69,5.86,6.11,5.81,5.62,5.70,5.81]
trasferta = [5.98,6.03,6.28,6.13,5.78,6.20,6.35,6.35,6.31]
prova = pd.DataFrame()
prova['HomeTeam'] = casa
prova['AwayTeam'] = trasferta
prova = sc_X.transform(prova)

pred = classifier.predict(prova)
results = classifier.predict_proba(prova)

#Visualizing the training set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min()-1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min()-1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1,X2,classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape), alpha = 0.75, cmap = ListedColormap(('red','blue','green')))
plt.xlim(X1.min(),X1.max())
plt.ylim(X2.min(),X2.max())
for i,j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set==j,0], X_set[y_set==j,1], c=ListedColormap(('red','blue','green'))(i), label=j)
plt.title('K-NN (training set)')
plt.xlabel('Home Team Strength')
plt.ylabel('Away Team Strength')
plt.legend()
plt.show()