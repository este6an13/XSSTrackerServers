import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sn
from joblib import dump, load


dataset = pd.read_csv(r'C:\Users\dquin072\Downloads\XSS_dataset1.csv')

X = dataset.iloc[:, 0:-1].values
y = dataset.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print(len(X_train), len(X_test))
print(len(y_train), len(y_test))

model = RandomForestClassifier(n_estimators=25, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(model.score(X_test, y_test))

cm = confusion_matrix(y_test, y_pred)

print(cm)
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

plt.figure(figsize=(10, 7))
sn.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')

plt.savefig('cm.png')

dump(model, 'rf_model.joblib')

md = load('rf_model.joblib')

for i, j in zip(range(0, 1000), range(1, 1001)):
    print(md.predict(X[i:j, :]))
