# Program that takes location of models and location of video 
# The video is classified separatly on each of the classifiers

import argparse
import os
import joblib
import numpy as np

from python_video_stream_pose_estimation import pose_est
from jab_preprocessing import return_elbow_sequence, return_overcommit_sequence


def jab_classifier(model_location, video_location):

    print(model_location)
    print(video_location)

    # Load all the models and save the Landmark Points that are required to predict a video with the corrisponding model.
    arm_protection_location = open(os.path.join(model_location, "KNN_arm_protection_06_05_21.pkl"), "rb")
    arm_protection_model = joblib.load(arm_protection_location)
    arm_protection_points = [0, 9, 10, 11, 12, 16, 18, 20]

    chin_protection_location = open(os.path.join(model_location, "KNN_chin_protected_06_05_21.pkl"), "rb")
    chin_protection_model = joblib.load(chin_protection_location)
    chin_protection_points = [0,9,10,11,12]

    elbow_out_location = open(os.path.join(model_location, "KNN_jab_elbow_06_05_21.pkl"), "rb")
    elbow_location_model = joblib.load(elbow_out_location)
    elbow_out_points = [11,12,13,15,23,24]

    overcommitment_location = open(os.path.join(model_location, "GradientBoost_overcommitting_06_05_21.pkl"), "rb")
    overcommitment_model = joblib.load(overcommitment_location)
    overcommitment_points = [0,9,10,11,12,23,24,25,26]

    right_elbow_location = open(os.path.join(model_location, "KNN_right_elbow_in_06_05_21.pkl"), "rb")
    right_elbow_model = joblib.load(right_elbow_location)
    right_elbow_points = [11, 12, 14, 24]

    # Get the list landmarks for each frame from BlazePose
    results = pose_est(video_location, show_images=False)

    #Preprocessing is required for Overcommitment & Checking whether elbows are sticking out while in jabbing motion
    #elbow_out_preprocessing = return_elbow_sequence(results)
    overcommitment_preprocessing = return_overcommit_sequence(results)

    # Requires individual lists on only the specified points
    arm_protection_results = extract_important_points(results, arm_protection_points)
    chin_protection_results = extract_important_points(results, chin_protection_points)
    elbow_out_results = extract_important_points(results, elbow_out_points)
    overcommitment_results = extract_important_points(overcommitment_preprocessing, overcommitment_points)
    right_elbow_results = extract_important_points(results, right_elbow_points)

    # Predict on results and model
    arm_protection_prediction = predict_clf(arm_protection_model, arm_protection_results)
    chin_protection_prediction = predict_clf(chin_protection_model, chin_protection_results)
    elbow_out_prediction = predict_clf(elbow_location_model, elbow_out_results)
    overcommitment_prediction = predict_clf(overcommitment_model, overcommitment_results)
    right_elbow_prediction = predict_clf(right_elbow_model, right_elbow_results)

    # Temporary print statements for CLI
    print("Arm Protection Prediction: {}".format(arm_protection_prediction))
    print("Chin Protection Prediction: {}".format(chin_protection_prediction))
    print("Elbow Out Prediction: {}".format(elbow_out_prediction))
    print("Overcommitment Prediction: {}".format(overcommitment_prediction))
    print("Right Elbow Prediction: {}".format(right_elbow_prediction))

    return generate_jab_feedback(arm_protection_prediction,
                          chin_protection_prediction,
                          elbow_out_prediction,
                          overcommitment_prediction,
                          right_elbow_prediction)


def extract_important_points(pose_result, feature_points):
    # feature_points refers to the landmarks which are required for the classifier e.g. arm_protection only considers the points 0 9 10 11 12 16 18 20 when classifying
    
    feature_points_results = [] # List of reduced frames

    # not_visible_landmarks_count = {}


    for frame in pose_result:
        feature_points_row = []
        visible = True # Boolean to determine if landmark is visible

        # Iterate through each of the 33 landmarks
        # disregard all other landmarks except ones required
        for i in range(33):
            if i in feature_points:
                # Now check if the landmark was visible
                if frame.landmarks[i][2] > 0.8 : # 80% visiblity threshold
                    feature_points_row.append((frame.landmarks[i][0], frame.landmarks[i][1]))

                else: # if landmark is not visible, than the whole frame has to be disregarded
                    visible = False
                    break

        if visible:
            feature_points_results.append(feature_points_row)
    
    return feature_points_results

def predict_clf(model, results):
    pred = {"0":0, "1":0}

    for row in results:
        # Convert into 1D numpy array
        np_frame = []

        for t in row:
            np_frame.append(t[0])
            np_frame.append(t[1])

        np_frame = np.array(np_frame)
        np_frame = np.asarray(np_frame).reshape(1, -1)

        # Feed to classifier
        est = str(model.predict(np_frame)[0])

        # Add to prediction dictionary
        pred[est] += 1

    return pred

# Two functions moved from jab_feedback.py to here as jab_feedback only gets called from within this prgram
# This program is to generate a feedback report given the predictions from classifier programs
# For now jab_classifier is the only classifier

#Currently for printing out to CLI

def generate_jab_feedback(AP_pred, CP_pred, EO_pred, OC_pred, RE_pred):
    # AP - Arm Protection
    # CP - Chin Protection
    # EO - Elbow Out (During Jab)
    # OC - Over Commmiting
    # RE - Right Elbow (Protection)

    # This function returns the overall prediction for the classifiers in the form of a feedback dictionary.
    # This allows feedback reports to be saved as lightwieght dictionaries and used to generate feedback reports when requested.
    # This program should also consider the number of frames predicted; if it is very little then the prediction shuld perhaps not be considered.

    feedback_dic = {}

    # Prediction  results
    AP_result = done_correctly(AP_pred)
    CP_result = done_correctly(CP_pred)
    EO_result = done_correctly(EO_pred, elbow_out=True) # threshold for predicting elbow out as only a few frames have elbow out
    OC_result = done_correctly(OC_pred)
    RE_result = done_correctly(RE_pred)

    # Build feedback report dictionary

    if AP_result == True:
        feedback_dic['1'] = 1

    elif AP_result == False:
        feedback_dic['1'] = 0

    else:
        feedback_dic['1'] = 2

    if CP_result == True:    
        feedback_dic['2'] = 1

    elif CP_result == False:
        feedback_dic['2'] = 0

    else:
        feedback_dic['2'] = 2

    if EO_result == True:
        feedback_dic['3'] = 1

    elif EO_result == False:
        feedback_dic['3'] = 0

    else:
        feedback_dic['3'] = 2

    if OC_result == True:
        feedback_dic['4'] = 1

    elif OC_result == False:
        feedback_dic['4'] = 0

    else:
        feedback_dic['4'] = 2

    if RE_result == True:
        feedback_dic['5'] = 1

    elif RE_result == False:
        feedback_dic['5'] = 0

    else:
        feedback_dic['5'] = 2


    return feedback_dic

def done_correctly(pred_dic, elbow_out=False):
    # return none if number of predictions less than threshold
    # return true if more positive label predictions than negative
    # return false if negative predictions more than or equal to positive predictions
    if pred_dic['0'] + pred_dic['1'] < 5:
        return None

    if not elbow_out:
        return True if pred_dic['0'] > pred_dic['1'] else False

    else:
        # 65 / 35 split i.e. should be over 65 percent correct to be predicted as correct
        return True if (pred_dic['0'] * 0.65) > (pred_dic['1'] * 0.35) else False


def main():
    parser = argparse.ArgumentParser(description='Classifies jab action on multiple features')
    parser.add_argument('--model-location', action='store', type=str, required=True)
    parser.add_argument('--video-location', action='store', type=str, required=True)

    args = parser.parse_args()

    jab_classifier(args.model_location, args.video_location)


if __name__ == '__main__':
    main()
