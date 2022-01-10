# For locally running scripts:

### auto_sklearn_classifier.py
Program which attempts to make the best model for predicting a given dataset  
Takes an hour to run and recieved 50% accuracy  
To run:
`python3 auto_sklearn_classifier.py PATH_TO_MODELS NAME_OF_MODEL`

### Body_Landmarks.py
Class to hold all 32 human pose landmarks for a particular frame  

### cleansing_images.py
This program has been deprecated by a function in ../Dataset_Code/make_dataset_numpy.py.  
`python3 cleansing_images.py PATH_TO_COLLECTION_OF_FRAMES`

### form_func_container.py
This program has been deprecated by our jab_classifier program. Previously this program calculates angles and distances between landmarks. Now we use machine learning models.

### Frame_Collection.py
Object which contains a collection of BodyLandmarks objects.

### jab_classifier.py
Program that takes location of models and location of video.  
The video is classified separatly on each of the classifiers.  
`python3 jab_classifier MODELS_LOCATION VIDEO_LOCATION`

### jab_feedback.py
This program is to generate a feedback dictionary report given the predictions from classifier programs.

### jab_preprocessing.py
Program which contains multiple functions which take in video sequences of jabs and the pose estimation results, and returns a cropped version of the video depending on the function called.  
This program should only be called externally and not from within the program itself.

### model_benchmark.py
This script uses multiple classifiers and machine learning algorithms and outputs the Accuracy of Testing Dataset and Validation Datasets given the Training Datasets. The path given must be in line with the appropriate directory format convention.  
`python3 model_benchmark.py PATH_TO_DATA` 

### pose_est_single_image.py
This program is for testing Pose Estimation on a single image displays the image with landmarks over the it.   
`python3 pose_est_single_image PATH_TO_IMAGE` 

### pose_estimation_controller.py
This program is no longer used, kept for legacy purposes.

### python_single_image_post_estimation.py
Depricated file is now contained in pose_est_single_image.py

### python_video_stream_estimation.py
This contains a function which is used in production and returns the pose estimation of a single video.

### random_forest_classifier.py
Originally we were going to use random forest classifier for creating our model but after extensive research thanks to model_benchmark.py we decided on a different machine learning algorithm.  
`python3 random_forest_classifier.py MODELS_LOCATION NAME_OF_MODEL LANDMARKS`

### model_image_testing.py
Program to test models on images  
`python3 train_classifier MODEL_LOCATION IMAGE_LOCATION`

### train_classifier.py
Program to train a QDA classifier  
`python3 train_classifier DATASET_LOCATION NAME_OF_MODEL`
