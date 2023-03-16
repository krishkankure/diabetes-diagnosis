import numpy as np
import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import sklearn.metrics
import pickle
from sklearn import datasets, metrics, model_selection, svm, tree
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
# ^^^

# creates input set
X = diabetes_data.drop(columns=['Outcome'])
# create output set
y = diabetes_data['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = pickle.load(open('model.pkl', 'rb'))

### MODEL PREDICTION ###
output = model.predict(X_test.values)

#### ACCURACY SCORE
accuracy = accuracy_score(y_test, output)

# use model to predict probability that given y value is 1

y_pred_proba = model.predict_proba(X_test)[::, 1]
conf_matrix = np.array([[280, 20], [21, 174]])
# calculate AUC of model
auc = sklearn.metrics.roc_auc_score(y_test, y_pred_proba)

# clf = svm.SVC(random_state=0)
# clf.fit(X_train, y_train)
# metrics.plot_roc_curve(clf, X_test, output)

# fig, ax = plt.subplots(figsize=(7.5, 7.5))
# ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
# for i in range(conf_matrix.shape[0]):
#    for j in range(conf_matrix.shape[1]):
#        ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')

# plt.xlabel('Predictions', fontsize=18)
# plt.ylabel('Actuals', fontsize=18)
# plt.title('Confusion Matrix', fontsize=18)
# plt.show()
clf = tree.DecisionTreeClassifier(random_state=1234)
clf = clf.fit(X_train, y_train)
tree.plot_tree(clf)
text_representation = tree.export_text(clf)
