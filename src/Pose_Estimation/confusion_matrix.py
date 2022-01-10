# Program to train a QDA classifier

import numpy as np
import sys, os, joblib
import argparse
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
import scikitplot as skplt
from sklearn import metrics

# Model
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# Metrics
from sklearn.metrics import classification_report, confusion_matrix

# Custom libraries
from python_video_stream_pose_estimation import pose_est
from pose_est_single_image import get_body_landmark # for validation

# import function to run QDA against testing set
from model_benchmark import testing_set_accuracy

def train_classifier(clf, location, model_name, save_location="", output_to_file=False):
    # Save location from which function was called; diagrams will be saved here
    if save_location == "":
        save_location = os.getcwd()

    
    # Check if output should be put to file. If so, switch the output stream to a file
    if output_to_file:
        # Set standard output to file
        os.chdir(save_location)
        orig_stdout = sys.stdout
        f = open('{:}_results.txt'.format(model_name.split(".")[0]), 'w')
        sys.stdout = f

    os.chdir(location)

    # Load in dataset by assuming the first file encounter with an "X" and "y" are the dataset, and extract important / specific points
    for file in os.listdir():
        
        if file[0].strip() == "X" and file.split(".")[-1].strip() == "joblib":
            # Read in X
            pickle_in = open(file,"rb")
            X = joblib.load(pickle_in)
            print("JOBLIB X done")

            # read in y assuming the file exists
            pickle_in = open("y{:}".format(file[1:]),"rb")
            y = joblib.load(pickle_in)
            print("JOBLIB y done")

            # Extract important points
            try: 
                i_p = [int(n) for n in ((file.split(".")[0]).split("_")[-1]).split(",")]
            except:
                print("The file found, '{:}', did not follow naming convention, please check local files. Exiting...".format(file))

    # Prepare data
    num_features = X.shape[1]

    X = X.reshape(X.shape[0], num_features*2) # reshape for sklearn models
    
    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("==========")
    print("Training : ", model_name)
    print("==========")
    
    # Train
    y_score = clf.fit(X_train, y_train)

    # Test validation
    score = clf.score(X_test, y_test)
    print("Model achieved the following validation score in training : ", score)

    # Estimate accuracy with testing set
    count, total = testing_set_accuracy(clf, location, i_p)
    print("Number correct in validation : {:}, out of {:}".format(count, total))
    print("Testing accuracy : {:.2f}".format((count / total) * 100))

    # Output f1 score and validation report
    y_pred = clf.predict(X_test)
    y_true = [int(label) for label in y_test]

    print(classification_report(y_pred, y_true, target_names=["Correct", "Incorrect"]))

    
    cf_matrix = confusion_matrix(y_pred, y_test)


    import seaborn as sns
    
    ax = plt.axes()

    sns_plot = sns.heatmap(cf_matrix, ax=ax, annot=True)

    ax.set_title("{:}".format(model_name.split(".")[0]))
    
    plt.show()

    # Save confusion matrix
    os.chdir(save_location)

    fig = sns_plot.get_figure()
    
    fig.savefig("{:}.png".format(model_name.split(".")[0]))

    plt.close()

    sys.stdout = orig_stdout


def main():
    # Example call : python model_benchmark.py "C:\Users\ohanl\Documents\CA400-Project\CA400-videos\Hands_up" hands

    parser = argparse.ArgumentParser(description='Roc Curve and Confusion Matrix producer')
    parser.add_argument('--dataset-location', action='store', type=str, required=True)
    parser.add_argument('--body-part', action='store', type=str, required=True)

    args = parser.parse_args()

    clf = QuadraticDiscriminantAnalysis() # Classifier

    import datetime
    model_name = "QDA_{:}_{:}.pkl".format(args.body_part, datetime.datetime.today().strftime('%d_%m_%y'))

    # Specific variable tells function that on specific points out 33 landmarks are in the dataset
    save_location = os.path.join(os.getcwd(), "..", "Model_Results")
    print(save_location)

    train_classifier(clf, str(args.dataset_location), model_name, save_location, output_to_file=True)

if __name__ == '__main__':
    main()