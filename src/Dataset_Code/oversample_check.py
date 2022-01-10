# program to test for oversampling in an existing numpy dataset

import sys, os, joblib
from make_dataset_numpy import check_oversampling_np

# Get file and file names off commandline
PATH = sys.argv[1]
NAME = sys.argv[2]
os.chdir(PATH)

# load in dataset
_in = open("X_{:}.joblib".format(NAME),"rb")
X = joblib.load(_in)
print("JOBLIB X done")


_in = open("y_{:}.joblib".format(NAME),"rb")
y = joblib.load(_in)
print("JOBLIB y done")

# Run check for oversampling
X, y = check_oversampling_np(X, y)
