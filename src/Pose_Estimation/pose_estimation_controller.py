import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import sys, os
import mediapipe as mp

# Custom libraries
from Body_Landmarks import Body_Landmarks
from Frame_Collection import Frame_Collection
import form_func_container

def pose_est(video_file=""):
    # Global variables used in both functions
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) # Setting static mode to false tells BlazePose that the input is a video stream and not single images

    # Prepare DrawingSpec for drawing landmarks
    mp_drawing = mp.solutions.drawing_utils 
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    cap = cv2.VideoCapture(0)

    #lst_frames = [] # lst to hold all data taken from each frame during pose estimation
    lst_frames = Frame_Collection("strike")
    i = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Reached end of video")
            break
        
        # Take every second frame to reduce computations and increase speed and performance
        if i % 2 == 0:

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.

            image.flags.writeable = False
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image_height, image_width, _ = image.shape

            if not results.pose_landmarks:
                continue

            landmark_lst = []
            i = 0
            for landmark in results.pose_landmarks.landmark:
                landmark_lst.append(landmark)

            tmp_landmark = Body_Landmarks(landmark_lst)#, image_width, image_height) # store data temporarily
            
            # Add frame to frame collection
            lst_frames.add(tmp_landmark)

            # Format image for output
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # output stance info to commandline
            form_func_container.live_stance_check(tmp_landmark)
             
            # results.pose_landmarks is a "landmark_list: A normalized landmark list proto message to be annotated on the image."
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # mp_pose.POSE_CONNECTIONS is just which points are connected e.g left_elbow to left_wrist

        if cv2.waitKey(5) & 0xFF == 27:
            print("Esc pressed, halting video")
            break
        i += 1

    pose.close()
    cap.release()

    return lst_frames # returns Frame_Collection object