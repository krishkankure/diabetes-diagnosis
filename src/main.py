## import numpy as np
import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sklearn.metrics
import pickle
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
# loads the data set

diabetes_data = pd.read_csv("diabetes.csv")

# X3['Pregnancies'] = diabetes_data['Pregnancies']
#^^^

# creates input set
X = diabetes_data.drop(columns=['Outcome'])
# create output set
y = diabetes_data['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

model = pickle.load(open('model.pkl', 'rb'))

### MODEL PREDICTION ###
output = model.predict(X_test.values)


#### ACCURACY SCORE
score = accuracy_score(y_test, output)


#use model to predict probability that given y value is 1

y_pred_proba = model.predict_proba(X_test)[::,1]

#calculate AUC of model
auc = sklearn.metrics.roc_auc_score(y_test, y_pred_proba)

# Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
df = pd.DataFrame()
preg = [1]
gluc = [2]
bp = [1]
st = [2]
ins = [1]
bmi = [2]
dpf = [1]
age = [2]
df['Pregnancies'] = preg
df['Glucose'] = gluc
df['BloodPressure'] = bp
df['SkinThickness'] = st
df['Insulin'] = ins
df['BMI'] = bmi
df['DiabetesPedigreeFunction'] = dpf
df['Age'] = age
print(model.predict_proba(df))
print(model.predict(df))