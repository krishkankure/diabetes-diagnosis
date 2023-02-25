## import numpy as np
import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import sklearn.metrics
import pickle
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
# loads the data set
import numpy as np
from pretty_confusion_matrix import pp_matrix, pp_matrix_from_data

diabetes_data = pd.read_csv("diabetes.csv")

# X3['Pregnancies'] = diabetes_data['Pregnancies']
#^^^

# creates input set
X = diabetes_data.drop(columns=['Outcome'])
# create output set
y = diabetes_data['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

model = pickle.load(open('model.pkl', 'rb'))

### MODEL PREDICTION ###
output = model.predict(X_test.values)


#### ACCURACY SCORE
accuracy = accuracy_score(y_test, output)

#use model to predict probability that given y value is 1

y_pred_proba = model.predict_proba(X_test)[::,1]
cm = confusion_matrix(y_test, output)
#calculate AUC of model
auc = sklearn.metrics.roc_auc_score(y_test, y_pred_proba)
print(type(cm))

# get pandas dataframe
df_cm = pd.DataFrame(cm, index=range(1, 3), columns=range(1, 3))
# colormap: see this and choose your more dear
cmap = 'PuRd'
pp_matrix(df_cm, cmap=cmap)
# Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
pp_matrix_from_data(y_test, output, cmap=cmap)