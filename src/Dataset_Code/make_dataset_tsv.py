import sys, os
import pandas as pd
from tqdm import tqdm

# Custom library
sys.path.append("../Pose_Estimation")
from python_video_stream_pose_estimation import pose_est
from jab_preprocessing import return_elbow_sequence, return_overcommit_sequence

def make_dataset(location):
    # For each video in the file location, call pose est and add results to dataset

    os.chdir(location) # change file location
    row_lst = [["Label", 'NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'LEFT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']]
    
    folders = os.listdir(location)[:] # Abstracted from file changes
    #print(folders)

    for folder in folders:
        # All folders containing video data follow this naming convention
        if str(folder.split("_")[0]) == "video":
            
            print("Processing {:}".format(os.path.join(location, folder)))
            label = int(folder.split("_")[1]) # label of videos

            for video in tqdm(os.listdir(os.path.join(location, folder))):

                if (video.split(".")[-1]).strip() == "mp4": # only want videos
                    print("Processing : ", video)

                    results = pose_est(os.path.join(location, folder, video), show_images=False) # call pose estimation
                    
                    # For each frame in results, add to row_lst
                    for frame in results:
                        data = [label, frame.landmarks]
                        # Frames in data are in x, y, visibility format, must change this to a string
                        #print(data)
                        row_lst.append(data) # add data

    return row_lst

def out_to_tsv(data, location):
    # Output data to dataset.tsv in location directory
    dataset = pd.DataFrame(data)
    dataset.to_csv(os.path.join(location, "dataset.tsv"), sep="\t") # save as tsv


def main():
    # This program is to make a custom dataset from specific local data

    # Take file location of video for datatset off of commmandline
    VIDEO_LOCATION = sys.argv[1]

    # Send resulting frames to make_datatset
    result = make_dataset(VIDEO_LOCATION)

    # Output data to file
    out_to_tsv(result, VIDEO_LOCATION)

if __name__ == '__main__':
    main()