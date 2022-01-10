# For locally running scripts:
This directory is for easily creating, sanitising and displaying datasets

### convert_video_to_images.py
Program to convert videos into frames for dataset preparation  
This is done to manually delete unnecessary / mislabelled frames
`python3 convert_video_to_images LOCATION_OF_FRAMES`

### dataset_script_windows.bat
Script that creates datasets through make_dataset_numpy.py
`bash dataset_script_windows.bat`

### display_existing_dataset.py
Code to run through and display each body landmark in a data csv  
This is as a quality assurance measure
`python3 display_existing_dataset DATA_LOCATION DATA_NAME`

### display_video_info.py
Script to convert a single video into a sequential dataset of pose estimated landmarks, and display this datset. Used for testing purposes.
`python3 display_video_info.py VIDEO_LOCATION`

### make_dataset_numpy.py
Similar to make_dataset_tsv.py except dataset is serialised as a numpy array along with respective labels. Also contains some dataset sanitation measures such as removing back frames recieved from pose estimation and deals with oversampling of the data
`python3 make_dataset_numpy.py VIDEO_LOCATION DATA_NAME`

### make_dataset_tsv.py
Dataset is serialised as a tsv file along with respective labels.
`python3 make_dataset_tsv.py VIDEO_LOCATION DATA_NAME`

### make_specific_dataset_numpy.py
This program is similar to previous dataset programs, except it takes datapoints as input and excludes those which are not included in the input
`python3 make_specific_dataset_numpy.py VIDEO_LOCATION DATA_NAME`

### oversample_check.py
This program is now imbedded within make_dataset_numpy.py
`python3 oversample_check.py VIDEO_LOCATION DATA_NAME`
