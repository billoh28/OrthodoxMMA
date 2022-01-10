import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import sys, os
import mediapipe as mp

# Custom libraries
from Body_Landmarks import Body_Landmarks
from Frame_Collection import Frame_Collection


def pose_est(video_file="", show_images=True):
    # Global variables used in both functions
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) # Setting static mode to false tells BlazePose that the input is a video stream and not single images

    # Prepare DrawingSpec for drawing landmarks
    mp_drawing = mp.solutions.drawing_utils 
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    # This will change depending on whether reading from file or webcam
    prv_cwd = os.getcwd()
    if len(video_file) > 0:
        # Change the file directory to where this file is located
        path, file = os.path.split(video_file)

        # Change path
        os.chdir(path)

        # open capture stream
        cap = cv2.VideoCapture(file)

    else:
        cap = cv2.VideoCapture(0)

    # Get dimensions from video
    width = int(cap.get(3))
    height = int(cap.get(4))

    #print(width, height)

    # Must ensure that aspect ratio of video is consistent.

    lst_frames = Frame_Collection("strike")#, width, height) # Object to hold all data taken from each frame during pose estimation
    
    i = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Reached end of video")
            break
        

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.

        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image_height, image_width, _ = image.shape

        # List of landmarks
        lst_points = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'LEFT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

        #print(mp_pose.POSE_CONNECTIONS, results.pose_landmarks)

        if not results.pose_landmarks:
            continue
        
        landmark_lst = []
        for landmark in results.pose_landmarks.landmark:
            #print("{:} : x = {:}, y = {:}, visibility = {:}".format(lst_points[i], landmark.x, landmark.y, landmark.visibility))
            landmark_lst.append(landmark)

        tmp_landmark = Body_Landmarks(landmark_lst, image_width, image_height) # store data temporarily
        
        # Add frame to frame collection
        lst_frames.add(tmp_landmark)

        if show_images:
            # Format image for output
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Add right arm info
            right_arm_angle_text = "Right Elbow to Hip Angle: {:.2f}".format(tmp_landmark.angle_between_landmarks(14, 12, 24))
            image = cv2.putText(image, right_arm_angle_text, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), cv2.LINE_4)

            # Add left arm info
            left_arm_angle_text = "Left Elbow to Hip Angle: {:.2f}".format(tmp_landmark.angle_between_landmarks(11, 13, 15))
            image = cv2.putText(image, left_arm_angle_text, (0, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), cv2.LINE_4)

            # output stance info to commandline
            #form_func_container.live_stance_check(tmp_landmark)
             
            # "landmark_list: A normalized landmark list proto message to be annotated on the image."
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # mp_pose.POSE_CONNECTIONS is just which points are connected e.g left_elbow to left_wrist

            cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(5) & 0xFF == 27:
            print("Esc pressed, halting video")
            break
        i += 1

    pose.close()
    cap.release()

    os.chdir(prv_cwd)

    return lst_frames # returns Frame_Collection object


def main():
    # Run this program either against input from the webcam or against an inputted video
    # This program will check for commandline arguments
    # If there are commmandline arguments the program assumes that this is a video file location and attempts to use that as input to BlazePose
    # If there are no commandline arguments input from the local webcam is fed to BlazePose instead

    # Check if commandline arguments provided
    if len(sys.argv) > 1:
        # Assume video file location provided
        VIDEO_LOCATION = sys.argv[1]
        results = pose_est(VIDEO_LOCATION)

    else:
        # Run against webcam
        results = pose_est()

    # Print resulting data
    # for l in results:
    #     print(l)

    #form_func_container.jab_check(results)

if __name__ == '__main__':
    main()


# Output from mp_pose.POSE_CONNECTIONS
    # frozenset({(<PoseLandmark.LEFT_WRIST: 15>, <PoseLandmark.LEFT_THUMB: 21>), (<PoseLandmark.RIGHT_WRIST: 16>, <PoseLandmark.RIGHT_INDEX: 20>), 
    # (<PoseLandmark.RIGHT_PINKY: 18>, <PoseLandmark.RIGHT_INDEX: 20>), (<PoseLandmark.LEFT_EYE_OUTER: 3>, <PoseLandmark.LEFT_EAR: 7>), 
    # (<PoseLandmark.RIGHT_ELBOW: 14>, <PoseLandmark.RIGHT_WRIST: 16>), (<PoseLandmark.LEFT_HIP: 23>, <PoseLandmark.LEFT_KNEE: 25>), 
    # (<PoseLandmark.MOUTH_RIGHT: 10>, <PoseLandmark.MOUTH_LEFT: 9>), (<PoseLandmark.RIGHT_ANKLE: 28>, <PoseLandmark.RIGHT_HEEL: 30>), 
    # (<PoseLandmark.LEFT_SHOULDER: 11>, <PoseLandmark.LEFT_HIP: 23>), (<PoseLandmark.LEFT_ANKLE: 27>, <PoseLandmark.LEFT_FOOT_INDEX: 31>), 
    # (<PoseLandmark.RIGHT_HIP: 24>, <PoseLandmark.LEFT_HIP: 23>), (<PoseLandmark.RIGHT_EYE_OUTER: 6>, <PoseLandmark.RIGHT_EAR: 8>), 
    # (<PoseLandmark.LEFT_WRIST: 15>, <PoseLandmark.LEFT_PINKY: 17>), (<PoseLandmark.RIGHT_HIP: 24>, <PoseLandmark.RIGHT_KNEE: 26>), 
    # (<PoseLandmark.RIGHT_WRIST: 16>, <PoseLandmark.RIGHT_THUMB: 22>), (<PoseLandmark.RIGHT_EYE_INNER: 4>, <PoseLandmark.RIGHT_EYE: 5>), 
    # (<PoseLandmark.RIGHT_EYE: 5>, <PoseLandmark.RIGHT_EYE_OUTER: 6>), (<PoseLandmark.LEFT_HEEL: 29>, <PoseLandmark.LEFT_FOOT_INDEX: 31>), 
    # (<PoseLandmark.RIGHT_SHOULDER: 12>, <PoseLandmark.RIGHT_HIP: 24>), (<PoseLandmark.NOSE: 0>, <PoseLandmark.LEFT_EYE_INNER: 1>), 
    # (<PoseLandmark.LEFT_EYE_INNER: 1>, <PoseLandmark.LEFT_EYE: 2>), (<PoseLandmark.NOSE: 0>, <PoseLandmark.RIGHT_EYE_INNER: 4>), 
    # (<PoseLandmark.LEFT_SHOULDER: 11>, <PoseLandmark.LEFT_ELBOW: 13>), (<PoseLandmark.RIGHT_HEEL: 30>, <PoseLandmark.RIGHT_FOOT_INDEX: 32>), 
    # (<PoseLandmark.RIGHT_ANKLE: 28>, <PoseLandmark.RIGHT_FOOT_INDEX: 32>), (<PoseLandmark.LEFT_WRIST: 15>, <PoseLandmark.LEFT_INDEX: 19>), 
    # (<PoseLandmark.RIGHT_WRIST: 16>, <PoseLandmark.RIGHT_PINKY: 18>), (<PoseLandmark.LEFT_KNEE: 25>, <PoseLandmark.LEFT_ANKLE: 27>), 
    # (<PoseLandmark.RIGHT_SHOULDER: 12>, <PoseLandmark.LEFT_SHOULDER: 11>), (<PoseLandmark.RIGHT_KNEE: 26>, <PoseLandmark.RIGHT_ANKLE: 28>), 
    # (<PoseLandmark.RIGHT_SHOULDER: 12>, <PoseLandmark.RIGHT_ELBOW: 14>), (<PoseLandmark.LEFT_PINKY: 17>, <PoseLandmark.LEFT_INDEX: 19>), 
    # (<PoseLandmark.LEFT_EYE: 2>, <PoseLandmark.LEFT_EYE_OUTER: 3>), (<PoseLandmark.LEFT_ANKLE: 27>, <PoseLandmark.LEFT_HEEL: 29>), 
    # (<PoseLandmark.LEFT_ELBOW: 13>, <PoseLandmark.LEFT_WRIST: 15>)}

    # points = {
    #     NOSE : 0,
    #     LEFT_EYE_INNER : 1,
    #     LEFT_EYE : 2,
    #     LEFT_EYE_OUTER : 3,
    #     RIGHT_EYE_INNER : 4,
    #     RIGHT_EYE : 5,
    #     right LEFT_EYE_OUTER : 6,
    #     LEFT_EAR : 7,
    #     RIGHT_EAR : 8,
    #     MOUTH_LEFT : 9,
    #     MOUTH_RIGHT : 10,
    #     LEFT_SHOULDER : 11,
    #     RIGHT_SHOULDER : 12,
    #     LEFT_ELBOW : 13,
    #     RIGHT_ELBOW : 14,
    #     LEFT_WRIST : 15,
    #     RIGHT_WRIST : 16,

        #     LEFT_PINKY : 17,
        #     RIGHT_PINKY : 18,
        #     LEFT_INDEX : 19,
        #     RIGHT_INDEX : 20,
        #     LEFT_THUMB : 21,
        #     RIGHT_THUMB : 22,

    #     LEFT_HIP : 23,
    #     RIGHT_HIP: 24,

        #     LEFT_KNEE : 25,
        #     RIGHT_KNEE : 26,
        #     LEFT_ANKLE : 27,
        #     RIGHT_ANKLE : 28,
        #     LEFT_HEEL : 29,
        #     RIGHT_HEEL : 30,
        #     LEFT_FOOT_INDEX : 31,
        #     RIGHT_FOOT_INDEX : 32,
        # }