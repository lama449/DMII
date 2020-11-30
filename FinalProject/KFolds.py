'''
Alex Lam and Maria Davis
Data Mining II final project
11/15/2020

This python file does 10 k-fold cross validation with different classifiers and creates graphs for accuracy
from a 90/10 split
'''

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import KFold
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn_pandas import DataFrameMapper

# Load the data from reddit and the desired stock
reddit = 'wsb'
stockticker = 'amzn'

reddit_data = pd.read_csv(reddit + stockticker + '.csv')

# Training is the Sentiment and the number of posts, Target is the stock direction for the day
X = reddit_data[['Sentiment', 'Count']]
y = reddit_data['Direction']

# Maintains the data in a dataframe with a scaler
mapper = DataFrameMapper([(X.columns, StandardScaler())])
scaled_features = mapper.fit_transform(X.copy(), 2)
scaled_features_df = pd.DataFrame(scaled_features, index=X.index, columns=X.columns)

# Splits the data into 10 Kfolds
kf = KFold(n_splits=10, random_state=7, shuffle=True)
accuracy = []

# The different models we test the data on
bnb = BernoulliNB(**{'alpha': 1.0, 'fit_prior': True})
rf = RandomForestClassifier(**{'n_estimators': 100, 'criterion': 'gini'})
svc = SVC(gamma='scale')
logr = LogisticRegression(**{'dual': False})
knn = KNeighborsClassifier(**{'n_neighbors': 5, 'weights': 'uniform'})
mlp = MLPClassifier(**{'hidden_layer_sizes': (30, 30, 30), 'max_iter': 2000})

models = [bnb, rf, logr, knn, mlp, svc]
model_names = ['bnb', 'rf', 'logr', 'knn', 'mlp', 'svc']

# Creates graphs for every model with with the desired data
for name in range(len(model_names)):
       for index, (train, test) in enumerate(kf.split(X), 1):

              X_train = X.iloc[train]
              X_test = X.iloc[test]
              y_train = y.iloc[train]
              y_test = y.iloc[test]

              model = models[name]
              model.fit(X_train, y_train)
              predictions = model.predict(X_test)
              accuracy.append(accuracy_score(y_test, predictions))
              #print(confusion_matrix(y_test, predictions))
              #print(classification_report(y_test, predictions))

              #print('\n')

       y_pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
       plt.figure(figsize=(10, 5))
       plt.bar(y_pos, accuracy, align='center', alpha=1)
       axes = plt.gca()
       axes.set_ylim([0, 1])
       plt.ylabel('Percent Accuracy')
       plt.title('KFold cuts for ' + stockticker + ' with model ' + model_names[name] + ' from r/' + reddit)
       plt.savefig(reddit + stockticker +'KFolds' + model_names[name] + '.png')
       plt.clf()
       accuracy = []
