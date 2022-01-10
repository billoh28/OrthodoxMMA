# Similar to make_dataset_tsv.py except dataset is serialised as a numpy array along with respective labels

import sys, os
import numpy as np
from tqdm import tqdm

# Custom library
from make_dataset_tsv import make_dataset

def output_np_to_file(frames, location, name, important_points=[], exclude_points=False):
    os.chdir(location)

    import joblib, random

    # Number of points to consider  
    num_of_points = 33
    if exclude_points == True:
        num_of_points = len(important_points)

    random.shuffle(frames) # randomise order

    print(len(frames))

    # check for bad frames
    frames = remove_bad_frames(frames, important_points)

    X = []
    y = []

    for label, features in frames:
        # Need to convert 33 tuples in features into one 99 length feature list
        lst_features = []

        # Check if points should be excluded
        if exclude_points:
            for i in range(33): # 33 is number of extracted features
                if i in important_points:
                    lst_features.append(features[i][0])
                    lst_features.append(features[i][1])

        else:
            for t in features:
                lst_features.append(t[0])
                lst_features.append(t[1])
                #lst_features.append(t[2])
            
        # Save data
        X.append(lst_features)
        y.append(label)

    X = np.array(X).reshape(-1, num_of_points, 2) # ensure right size
    y = np.array(y)

    # Check for oversampling
    try:
        X, y = check_oversampling_np(X, y, num_of_points)
    except TypeError:
        sys.exit(1)

    # Output random row for quality check
    print(X[random.randint(0, X.shape[0])])

    assert X.shape[0] == y.shape[0]

    important_points = [str(n) for n in important_points]

    if exclude_points:
        # Serialise data
        out = open("X_{:}_{:}.joblib".format("".join(name.split(" ")), ",".join(important_points)),"wb")
        joblib.dump(X, out)
        out.close()

        out = open("y_{:}_{:}.joblib".format("".join(name.split(" ")), ",".join(important_points)),"wb")
        joblib.dump(y, out)
        out.close()

    else:
        # Serialise data
        out = open("X_{:}.joblib".format("".join(name.split(" "))),"wb")
        joblib.dump(X, out)
        out.close()

        out = open("y_{:}.joblib".format("".join(name.split(" "))),"wb")
        joblib.dump(y, out)
        out.close()

    print("Dataset of size {:} produced".format(X.shape))

# Function to check and amend oversampling in labelled numpy dataset
def check_oversampling_np(X, y, num_features=33):
    import random

    label_count = {}

    # Must contain the same number of rows
    assert X.shape[0] == y.shape[0]

    for i in tqdm(range(X.shape[0])):
        label = y[i]
        if label not in label_count:
            label_count[label] = 1
        else:
            label_count[label] += 1

    print(label_count)

    try:
        min_count = min(label_count.values()) # count of the most undersampled label

    except ValueError:
        print("Dataset not loaded, change directory names to required format e.g. 'video_0'")
        return 

    # Recombine dataset and randomly remove excess rows
    comb_dataset = []
    for i in range(X.shape[0]):
        comb_dataset.append([y[i], list(X[i])])

    random.shuffle(comb_dataset) # randomise order

    # Remove oversampling
    new_X = []
    new_y = []

    label_count = {}

    for label, features in comb_dataset:
        if label not in label_count:
            label_count[label] = 1
        else:
            if label_count[label] < min_count:
                # Save data
                new_X.append(features)
                new_y.append(label)
                label_count[label] += 1

    print(label_count)
    return np.array(new_X).reshape(-1, num_features, 2), np.array(new_y)

# Function which takes a dataset of BlazePose predictions and removes those which have bad visibility for the important points
def remove_bad_frames(frames, important_points=[]):

    num_of_points = len(important_points)
    # Check if important_points is empty, ignore and return
    if num_of_points == 0:
        return frames

    cleaned_frames = []

    # Count number of specific landmarks which were below threshold
    failed_landmarks = {}

    for point in important_points:
        failed_landmarks[point] = 0
    print(failed_landmarks)

    for label, features in frames:
        is_ignored = False
        for p in important_points:
            # Check if visibility under threshold, and if so ignore row
            if float(features[p][2]) < 0.8:
                is_ignored = True
                failed_landmarks[p] = failed_landmarks[p] + 1

        if is_ignored:
            #print(features)
            pass

        else:
            cleaned_frames.append([label, features])


    landmarks_names = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'LEFT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']
    
    # Output results
    for k, v in failed_landmarks.items():
        print("No. bad '{:}({:})' landmarks: {:}".format(landmarks_names[k], k, v)) 

    # Return results
    return cleaned_frames


def main():
    # This program is to make a custom dataset from specific local data
    # e.g. python make_dataset_numpy.py "C:\Users\ohanl\Documents\CA400-Project\CA400-videos\Hands_up" hands 11 12 13 14 23 24 25 26 27 28 29 30 31 32

    landmarks_names = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'LEFT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

    # Take file location of video for datatset off of commmandline
    VIDEO_LOCATION = sys.argv[1]

    # Take name off commandline
    NAME = sys.argv[2]

    # required variables
    important_points = []
    exclude_points = False

    '''
    if len(sys.argv) > 3: # Important points provided

        # Check if only these points should be included in the dataset
        print("The points provided correspond to the following landmarks respectively : {:}".format([landmarks_names[i] for i in important_points]))
        print("Should only these points be considered in the dataset? (y/n)")

        answer = input()

        if answer.lower() == "y":
    '''
    exclude_points = True
    important_points = [int(n) for n in sys.argv[3:]]
    print("The points provided correspond to the following landmarks respectively : {:}".format([landmarks_names[i] for i in important_points]))

    
    # Send resulting frames to make_datatset
    result = make_dataset(VIDEO_LOCATION)

    #print(result)

    # Send frames to numpy array handler
    output_np_to_file(result[1:], VIDEO_LOCATION, NAME, important_points, exclude_points) # ignore first element in result as it is csv headers

if __name__ == '__main__':
    main()