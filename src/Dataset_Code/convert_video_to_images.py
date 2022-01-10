# Program to convert videos into frames for dataset preparation
# This is done to manually delete unnecessary / mislabelled frames

import cv2, sys, os
from tqdm import tqdm


def main():
    # Take video location and frame name off commandline
    vid_location = sys.argv[1] # Folder containing videos

    # Take name of folders off cmd line 
    name_1 = sys.argv[2]
    name_2 = sys.argv[3]

    os.chdir(vid_location) # Set working dir to vid location

    required_name = "fitness_poses_images_in"

    if not os.path.exists(os.path.join(os.getcwd(), required_name)):
        # Make the dir if it does not exist
        os.mkdir(os.path.join(os.getcwd(), required_name))

    if not os.path.exists(os.path.join(os.getcwd(), required_name, name_1)):
        # Make the dir if it does not exist
        os.mkdir(os.path.join(os.getcwd(), required_name, name_1))

    if not os.path.exists(os.path.join(os.getcwd(), required_name, name_2)):
        # Make the dir if it does not exist
        os.mkdir(os.path.join(os.getcwd(), required_name, name_2))

    count = 0

    for video in tqdm(os.listdir()):
        # Determine whether correct or incorrect label
        is_correct = True

        if video.split("_")[1].strip() == "incorrect":
            is_correct = False

        if (video.split(".")[-1]).strip() == "mp4": # only want videos
            # Read video
            videoCapture = cv2.VideoCapture(os.path.join(os.getcwd(), video))
            success, image = videoCapture.read()

            if is_correct:
                os.chdir(os.path.join(os.getcwd(), required_name, name_1))
                name = name_1

            else:
                os.chdir(os.path.join(os.getcwd(), required_name, name_2))
                name = name_2

            while success:
                cv2.imwrite("{:}_{:}.jpg".format(name, count), image)     # save frame as JPEG file      
                success, image = videoCapture.read()
                #print('Saved a new frame: ', success)
                count += 1

        os.chdir(vid_location) # Set working dir to vid location

if __name__ == '__main__':
    main()