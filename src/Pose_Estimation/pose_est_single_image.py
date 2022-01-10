import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

from Body_Landmarks import Body_Landmarks


def get_body_landmark(image_location):

    img_array = cv2.imread(image_location, cv2.IMREAD_UNCHANGED) # convert to array
    
    image_height, image_width, _ = img_array.shape

    # Adapted from notebook obtained through MediaPipe Pose Estimation Python documentation: https://google.github.io/mediapipe/solutions/pose#python-solution-api

    import mediapipe as mp
    mp_pose = mp.solutions.pose

    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

    # Convert the BGR image to RGB and process it with MediaPipe Pose.
    results = pose.process(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

    landmark_lst = []
    for landmark in results.pose_landmarks.landmark:
        #print(results.pose_landmarks.landmark)
        #print("{:} : x = {:}, y = {:}, visibility = {:}".format(lst_points[i], landmark.x, landmark.y, landmark.visibility))
        landmark_lst.append(landmark)

    tmp_landmark = Body_Landmarks(landmark_lst)#, image_width, image_height) # store data temporarily

    return tmp_landmark

def main():
    test_image = sys.argv[1] # Enter test file on the commandline

    landmark = get_body_landmark(test_image)

    print(landmark)

if __name__ == '__main__':
    main()