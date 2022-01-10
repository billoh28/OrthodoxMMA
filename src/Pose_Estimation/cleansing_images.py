'''
This program has been deprecated by a function in ../Dataset_Code/make_dataset_numpy.py.
'''

import cv2, sys, os
from os import listdir
from os.path import isfile, join
from pose_est_single_image import get_body_landmark

# Take video location and frame name off commandline
frames_location = sys.argv[1] # Folder containing frames

#for frame in location
# pass the image into pose estimation and if it returns that the 
# key points such as hands elbows and shoulders are not found, 
# we dispose of the images

important_landmarks = [11,12,13,14,15,16]

deleted = 0

# os.chdir(frames_location) # Set working dir to vid location
for path, subdirs, files in os.walk(frames_location):
    for name in files:
        single_frame_location = os.path.join(path, name) 
        remove_frame_cond = False
        if name.split(".")[1] == "jpg": #if the file is a jpg image
            print(single_frame_location)
            result = get_body_landmark(single_frame_location)
            frame = result.landmarks

            #if the frames landmarks in important landmarks is not completely visible delete the image
            for vital_land in important_landmarks:
            	if frame[vital_land][2] < 0.8:
            		remove_frame_cond = True

        if remove_frame_cond == True:
        	#Delete the image from the dataset
            #os.remove(single_frame_location)
            deleted += 1
        remove_frame_cond = False

print("{:} frames deleted".format(deleted))
