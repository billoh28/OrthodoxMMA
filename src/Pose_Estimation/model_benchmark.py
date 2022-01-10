import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

# Models
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis

# Metrics
from sklearn.metrics import classification_report

# Custom libraries
from python_video_stream_pose_estimation import pose_est



import sys, os, joblib

from pose_est_single_image import get_body_landmark # for validation

def testing_set_accuracy(clf, path, i_p=[]): # run given classifier against testing set stored at the given path

    os.chdir(os.path.join(path, "test_images"))

    count = 0 # count of number of imgs guessed correctly in validation
    total = 0 # total number of test images
    for file in os.listdir():
        #print("Testing : ", file)

        # Get label
        if file.split("_")[1].strip() == "correct":
            label = 0
        else:
            label = 1

        # Check if file in test set is video or image based
        if file.split(".")[-1] == "mp4":
            # Pass video to pose estimation
            results = pose_est(os.path.join(os.getcwd(), file), show_images=False) # call pose estimation

            new_results = []

            if len(i_p) > 0: # meaning some points have been removed from the dataset
                # remove these points from test video results

                for frame in results:
                    row = []
                    for i in range(33): # 33 is number of extracted features
                        if i in i_p:
                            # Add to new results
                            row.append((frame.landmarks[i][0], frame.landmarks[i][1]))

                    new_results.append(row)

            else:
                for frame in results:
                    row = []
                    for t in frame.landmarks:
                        row.append((t[0], t[1]))
                    new_results.append(row)

            # AVERAGE ROLLING
            '''
            Feed each frame in results to the classifier. Save the prediction, and repeat.
            After this is done, get vthe average prediction over all frames to classify the video.
            '''
            pred = {"0":0, "1":0}

            for row in new_results:
                # Convert into 1D numpy array
                np_frame = []
                
                for t in row:
                    np_frame.append(t[0])
                    np_frame.append(t[1])
                    #np_frame.append(t[2])

                np_frame = np.array(np_frame)
                np_frame = np.asarray(np_frame).reshape(1, -1)

                # Feed to classifier
                est = str(clf.predict(np_frame)[0])

                # Add to prediction dictionary
                pred[est] += 1

            print(pred)

            # Final prediction
            if pred["0"] > pred["1"]:
                prediction = 0
            else:
                prediction = 1

        else:
            # Image based testing set
            # Pass image to BlazePose
            result = get_body_landmark(file)

            # Convert into format accepted by model i.e. 1D numpy array
            frame = result.landmarks # from Body_Landmark class

            # Convert into 1D numpy array
            np_frame = []
            
            for i in range(len(frame)):
                t = frame[i]

                if len(i_p) > 0: # meaning some points have been removed from the dataset
                    if i in i_p: # extract specific features
                        np_frame.append(t[0])
                        np_frame.append(t[1])

                else:
                    np_frame.append(t[0])
                    np_frame.append(t[1])

            np_frame = np.array(np_frame)
            np_frame = np.asarray(np_frame).reshape(1, -1)
            #print(np_frame)

            # Run test
            prediction = int(clf.predict(np_frame))

        if prediction == label:
            count += 1

        # Output result
        #print("Result : ", prediction)

        total += 1

    # Reset path
    os.chdir(path)

    # Return preditctions
    return [count, total]



def main():
    # Example call : python model_benchmark.py "C:\Users\ohanl\Documents\CA400-Project\CA400-videos\Hands_up" hands --file
    PATH = sys.argv[1] # Path to files
    os.chdir(PATH)

    orig_stdout = sys.stdout
    # Check if output should be put to file. If so, switch the output stream to a file
    if sys.argv[3] == "--file":
        # Set standard output to file
        f = open('benchmark_results.txt', 'w')
        sys.stdout = f

    names = ["Gradient Boosting", "Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
             "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
             "Naive Bayes", "QDA"]

    classifiers = [
        GradientBoostingClassifier(n_estimators=10, learning_rate=0.1, max_depth=12),
        KNeighborsClassifier(2),
        SVC(kernel="linear", C=0.025),
        #SVC(gamma=2, C=1),
        #GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=12),
        RandomForestClassifier(max_depth=12, n_estimators=10, max_features=6),
        MLPClassifier(alpha=1, max_iter=1000),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis(),
        LinearDiscriminantAnalysis()]

    

    '''
    # load in dataset
    pickle_in = open("X_{:}.joblib".format(body_part),"rb")
    X = joblib.load(pickle_in)
    print("JOBLIB X done")


    pickle_in = open("y_{:}.joblib".format(body_part),"rb")
    y = joblib.load(pickle_in)
    print("JOBLIB y done")
    '''

    # Load in dataset by assuming the first file encounter with an "X" and "y" are the dataset
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
            if len(file.split("_")) > 2: # based on file naming conventions
                i_p = [int(n) for n in ((file.split(".")[0]).split("_")[-1]).split(",")]
            else:
                i_p = []
            print(i_p)

    num_features = X.shape[1]

    X = X.reshape(X.shape[0], num_features*2) # reshape for sklearn models

    #print(X.shape)
    import datetime
    print(datetime.datetime.today().strftime('%d_%m_%y'))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save model validation accuracy
    accur = 0

    # iterate over classifiers
    for name, clf in zip(names, classifiers):
        print("==========")
        print("Training : ", name)
        print("==========")
        clf.fit(X_train, y_train)

        # Test validation
        score = clf.score(X_test, y_test)
        print("Model achieved the following validation score in training : ", score)

        # Output f1 score and validation report
        y_pred = clf.predict(X_test)
        y_true = [int(label) for label in y_test]

        print(classification_report(y_pred, y_true, target_names=["Correct", "Incorrect"]))

        if score >= accur: # If accurate run tests
            # Update accur variable
            accur = score

            # Locally there is a file called test_images
            print("==========")
            print("Testing : ", name)
            print("==========")
            try:
                count, total = testing_set_accuracy(clf, PATH, i_p) # Estimate the accuracy of the model with the testing set
                print("Testing results : {:}, out of {:} ({:.2f}%)".format(count, total, (count/total)*100))

            except FileNotFoundError:
                print("File not found error occured...")

        print("==========")
        print("==========")
        print("==========")

    sys.stdout = orig_stdout

    # After testing, Adaboost scored the most correct with 19 out of 26 fo rthe hands dataset

if __name__ == '__main__':
    main()