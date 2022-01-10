from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys, os, time
import joblib
import datetime
import argparse
import numpy as np

# Custom libraries 
sys.path.append("../Dataset_Code")
from make_dataset_numpy import check_oversampling_np
from pose_est_single_image import get_body_landmark # for validation

def random_forest(model_location, body_part, split=[]):
    print(split)
    os.chdir(model_location)
    if len(split) > 0:
        # Assume a list is provided with the body points to be excluded
        is_split = True

    else:
        is_split = False

    # load in dataset
    pickle_in = open("X_{:}.joblib".format(body_part),"rb")
    X = joblib.load(pickle_in)
    print("JOBLIB X done")


    pickle_in = open("y_{:}.joblib".format(body_part),"rb")
    y = joblib.load(pickle_in)
    print("JOBLIB y done")

    # Max features for random forest to split on
    max_features = 33
    # Split list if necessary
    if is_split:
        # set certain features to zero based off split points list
        for feature in split:
            # Set this feature to zero
            X[:,int(feature)] = 0

        # Reduce max features
        max_features -= len(split)

    #print(X[28])

    X, y = check_oversampling_np(X, y)

    # Since sklearn only allows 2 dimensions, we must reshape
    X = X.reshape(X.shape[0], 33*2) # (x,y) as visibility has been taken out

    #print(X[28])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    clf = RandomForestClassifier(max_features, max_depth=None , random_state=0)

    clf.fit(X_train,y_train)

    landmarks_names = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'LEFT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

    feature_usage = clf.feature_importances_ # output feature importance
    for i in range(len(feature_usage)):
        if feature_usage[i] > 0:
            print("{:} : {:}".format(landmarks_names[i//3], clf.feature_importances_[i]))

    yhat = clf.predict(X_test)
    # evaluate predictions
    acc = accuracy_score(y_test, yhat)
    print('Accuracy: %.3f' % acc)

    # Name classifier
    if is_split:
        name = "random_forest_{:}_split_{:}.pkl".format(body_part, datetime.datetime.today().strftime('%m_%d'))

    else:
        name = "random_forest_{:}_{:}.pkl".format(body_part, datetime.datetime.today().strftime('%m_%d'))

    # Save classifier
    out = open(name,"wb")
    joblib.dump(clf, out)
    out.close()
    print("{:} classifier saved".format(name))

    # Test validation
    # Locally there is a file called validation_images
    try:
        os.chdir(os.path.join(os.getcwd(), "validation_images"))
        dic = {"correct" : 0, "incorrect" : 0}
        for img in os.listdir():
            print(img)

            # Pass image to BlazePose
            result = get_body_landmark(img)

            # Convert into format accepted by model i.e. 1D numpy array
            frame = result.landmarks # from Body_Landmark class

            # Convert into 1D numpy array
            np_frame = []
            
            for t in frame:
                np_frame.append(t[0])
                np_frame.append(t[1])
                #np_frame.append(t[2])

            np_frame = np.array(np_frame)
            np_frame = np.asarray(np_frame).reshape(1, -1)
            print(np_frame)

            # Run test
            prediction = clf.predict(np_frame)

            # Output result
            print(prediction)
            img_type = img.split(".")[0].split("_")[1]
            if img_type == "correct":
                dic["correct"] += 1
            else:
                dic["incorrect"] += 1

        print(dic)


    except FileNotFoundError:
        print("FileNotFound: cannot validate")

def main():
    parser = argparse.ArgumentParser(description='Random Forest Classifier functions')
    parser.add_argument('--model-location', action='store', type=str, required=True)
    parser.add_argument('--body-part', action='store', type=str, required=True)
    parser.add_argument('--landmarks-positions', nargs="*")

    args = parser.parse_args()

    print(args.model_location)

    if args.landmarks_positions == None:
        random_forest(args.model_location, args.body_part)

    else:
        random_forest(args.model_location, args.body_part, args.landmarks_positions)

    # Example 
    # python3 random_forest_classifier.py --model-location="/home/killian/Documents/datasets/Elbows_in/auto_ml_classifier_elbows.pkl" --body-part="elbows" --land 1 2 3 5

if __name__ == '__main__':
    main()
