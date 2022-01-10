# Program to test random forest on images

import sys
import joblib
import numpy as np
from pose_est_single_image import get_body_landmark

# Take model from cmd line
_in = open(sys.argv[1],"rb")
model = joblib.load(_in)
print("Model {:} loaded".format(sys.argv[1]))

# Load in image from cmd line
IMAGE_LOCATION = sys.argv[2]

# Pass image to BlazePose
result = get_body_landmark(IMAGE_LOCATION)

# Convert into format accepted by model i.e. 1D numpy array
frame = result.landmarks # from Body_Landmark class

# Convert into 1D numpy array
np_frame = []
for t in frame:
    np_frame.append(t[0])
    np_frame.append(t[1])
    # np_frame.append(t[2])

np_frame = np.array(np_frame)
np_frame = np.asarray(np_frame).reshape(1, -1)
print(np_frame)

# Run test
prediction = model.predict_proba(np_frame)

# Output result
print(prediction)
