# Code to run through and display each body landmark in a data csv
# This is as a quality assurance measure

import sys, os, joblib
import numpy as np
from matplotlib import pyplot as plt

# Get file and file names off commandline
PATH = sys.argv[1]
NAME = sys.argv[2]
os.chdir(PATH)

# load in dataset
pickle_in = open("X_{:}.joblib".format(NAME),"rb")
X = joblib.load(pickle_in)
print("JOBLIB X done")


pickle_in = open("y_{:}.joblib".format(NAME),"rb")
y = joblib.load(pickle_in)
print("JOBLIB y done")

# Test UPPER
#X = X[:,:25]

# Connections
connections = [(15,21),
    (16,20), 
    (18, 20),
    (3,7), 
    (14,16),
    (23,25), 
    (10, 9),
    (28, 30), 
    (11, 23),
    (27, 31), 
    (24, 23), 
    (6, 8), 
    (15, 17),
    (24, 26), 
    (16, 22),
    (4, 5), 
    (5, 6),
    (29, 31), 
    (12, 24),
    (0, 1), 
    (1, 2),
    (0, 4), 
    (11, 13),
    (30, 32), 
    (28, 32),
    (15, 19), 
    (16, 18),
    (25, 27), 
    (12, 11),
    (26, 28), 
    (12, 14),
    (17, 19), 
    (2,  3),
    (27, 29), 
    (13, 15)
    ]

for i in range(X.shape[0]):
    # display row
    x_points = []
    y_points = []
    for j in range(X.shape[1]):
        # iterate through landmarks in row
        x_points.append(2160 - int(X[i][j][0]))
        y_points.append(3840 - int(X[i][j][1]))

    # Plot x and y
    print("Label: {:}".format(y[i]))
    plt.scatter(x_points, y_points)

    # Connections
    for con in connections:
        # Display connections
        x1, x2 = x_points[con[0]], x_points[con[1]]
        y1, y2 = y_points[con[0]], y_points[con[1]]
        plt.plot([x1,x2],[y1,y2],'k-')

    #plt.ylim(0,3840)
    #plt.xlim(0,2160)

    # Show scatter plot
    plt.show()
