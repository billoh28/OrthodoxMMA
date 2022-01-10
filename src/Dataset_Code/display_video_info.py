# Program to convert a single video into a sequential dataset of pose estimated landmarks, and display this datset

# Used for testing only

# Third party libraries
import sys, os, joblib
import numpy as np
from matplotlib import pyplot as plt

# Custom libraries
sys.path.append("../Pose_Estimation")
from python_video_stream_pose_estimation import pose_est

# Video location
video = sys.argv[1]

# Create a list of a list of tuples
results = pose_est(video, show_images=False) # call pose estimation
frames = [frame.landmarks for frame in results]

# Connections
connections = [
    #(15,21),
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
    #(15, 17),
    (24, 26), 
    (16, 22),
    (4, 5), 
    (5, 6),
    (29, 31), 
    (12, 24),
    (0, 1), 
    (1, 2),
    (0, 4), 
    #(11, 13),
    (30, 32), 
    (28, 32),
    #(15, 19), 
    (16, 18),
    (25, 27), 
    (12, 11),
    (26, 28), 
    (12, 14),
    #(17, 19), 
    (2,  3),
    (27, 29), 
    #(13, 15)
    ]

for i in range(len(frames)):
    if i % 10 == 0:
        # display row
        x_points = []
        y_points = []
        for j in range(len(frames[i])):
            # iterate through landmarks in row
            x_points.append(2160 - int(frames[i][j][0]))
            y_points.append(3840 - int(frames[i][j][1]))

        # Plot x and y
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