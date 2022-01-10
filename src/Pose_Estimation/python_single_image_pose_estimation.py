import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys, os

from Body_Landmarks import Body_Landmarks

test_image = sys.argv[1] # Enter test file on the commandline

img_array = cv2.imread(test_image, cv2.IMREAD_UNCHANGED) # convert to array

image_height, image_width, _ = img_array.shape

# Adapted from notebook obtained through MediaPipe Pose Estimation Python documentation: https://google.github.io/mediapipe/solutions/pose#python-solution-api

import mediapipe as mp
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# Prepare DrawingSpec for drawing landmarks 
mp_drawing = mp.solutions.drawing_utils 
drawing_spec = mp_drawing.DrawingSpec(thickness=4, circle_radius=6, color=(255, 0, 0))

# Convert the BGR image to RGB and process it with MediaPipe Pose.
results = pose.process(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

# Output results to commandline
landmark_lst = []
for landmark in results.pose_landmarks.landmark:
    #print("{:} : x = {:}, y = {:}, visibility = {:}".format(lst_points[i], landmark.x, landmark.y, landmark.visibility))
    landmark_lst.append(landmark)

tmp_landmark = Body_Landmarks(landmark_lst, image_width, image_height) # store data temporarily

print(tmp_landmark)
print(tmp_landmark.landmarks[11])
print(tmp_landmark.landmarks[12])

# Annotate the image with the estimated landmarks
annotated_image = img_array.copy()
mp_drawing.draw_landmarks(image=annotated_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=drawing_spec, connection_drawing_spec=drawing_spec)
#print(results.pose_landmarks)

# Display the inputted image with the annotated pose estimation
cv2.imshow('image_2', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save image
cv2.imwrite(os.path.join(os.getcwd(), "test.jpg"), annotated_image) # filename, image

