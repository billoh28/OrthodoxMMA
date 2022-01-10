# Program which attempts to make the best model for predicting a given dataset
# Takes an hour to run
# When ran on Elbows In dataset, got 50% accuracy with test set

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys, os
import joblib
import datetime

sys.path.append("../Dataset_Code")
from make_dataset_numpy import check_oversampling_np


# Get file and file names off commandline
PATH = sys.argv[1]
NAME = sys.argv[2]
os.chdir(PATH)

# Get if upper from commandline
if len(sys.argv) > 3:
	is_upper = bool(sys.argv[3])

else:
	is_upper = False

# load in dataset
pickle_in = open("X_{:}.joblib".format(NAME),"rb")
X = joblib.load(pickle_in)
print("JOBLIB X done")


pickle_in = open("y_{:}.joblib".format(NAME),"rb")
y = joblib.load(pickle_in)
print("JOBLIB y done")

X, y = check_oversampling_np(X, y)

# Since sklearn only allows 2 dimensions, we must reshape
X = X.reshape(X.shape[0], 33*3)

if is_upper: # Remove landmarks from left_knee onwards from dataset
    # left knee is number 25
    X[:,25*3:] = 0

#print(X[28])
#print(X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

import autosklearn.classification
clf = autosklearn.classification.AutoSklearnClassifier()
print("hi")
clf.fit(X_train,y_train)

yhat = clf.predict(X_test)
# evaluate predictions
acc = accuracy_score(y_test, yhat)
print('Accuracy: %.3f' % acc)

name = "auto_ml_classifier_{}.pkl".format(NAME)
# Save classifier
out = open(name,"wb")
joblib.dump(clf, out)
out.close()

