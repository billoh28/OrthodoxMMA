# Program which contains multiple functions which take in video sequences of jabs and the pose estimation results, and returns a cropped version of the video depending on the function called
# This program should only be called externally and not from within the program itself

import sys

def return_elbow_sequence(pose_est): # pose_est is a frame collection object
    # Returns a frame collection object
    sys.path.append("../Pose_Estimation")
    from Frame_Collection import Frame_Collection
    # Given a frame.collection object of the pose estimations, return the frame collection but where the angle of the left arm, theta, is : 80 < theta < 170
    # So the indices of the points we care about are the one's which relate to the left shoulder, left elbow and the left wrist i.e. 11, 13 and 15 respectively
    desired_seq = Frame_Collection("jab")

    count = 0 # count for no. frames which satisfy condition, this helps prevent errors due to model flickering
    
    for frame in pose_est:
        # First get angle of left arm
        theta = frame.angle_between_landmarks(11, 13, 15)
        print(theta)

        # Check if theta makes condition
        if theta > 80 and theta < 170:
            desired_seq.add(frame)

    return desired_seq # Frame_Collection object



def return_overcommit_sequence(pose_est): # pose_est is a frame collection object
    # Same as above function only we wish to gather frames where the user is fully extended in the jab motion
    sys.path.append("../Pose_Estimation")
    from Frame_Collection import Frame_Collection
    
    desired_seq = Frame_Collection("jab")

    count = 0 # count for no. frames which satisfy condition, this helps prevent errors due to model flickering
    found = False # Setter to show found required frame sequence, this is important as we do not want the frames of the elbow on the way back from the jab 
    max_angle_achieved = 0

    for frame in pose_est:
        # First get angle of left arm
        theta = frame.angle_between_landmarks(11, 13, 15)

        # Save max angle    
        if theta > max_angle_achieved:
            max_angle_achieved = theta

        # Check if theta makes condition
        if theta > 100:
            count += 1
            if count > 2: # Count as an insurance against model flickering
                desired_seq.add(frame)
                found = True

        elif found: # i.e. sequence already found
            # Return sequnce
            print(max_angle_achieved)
            return desired_seq

    return desired_seq # Frame_Collection object


def main():
    # For testing the above functions only
    # This program should not be called directly in production

    # Take a video location from commandline, pass it to pose_est and give the results to the functions, then save resulting dataset

    import sys, os
    video = sys.argv[1]

    # Custom libraries
    sys.path.append("../Dataset_Code")

    from python_video_stream_pose_estimation import pose_est
    from make_dataset_numpy import output_np_to_file

    results = pose_est(video, show_images=False) # call pose estimation

    over_seq = return_overcommit_sequence(results)
    elbow_seq = return_elbow_sequence(results)

    # Add labels for testing with other programs. The value of the label doesn't actually matter
    over_seq = [[0, row] for row in over_seq]
    elbow_seq = [[0, row] for row in elbow_seq]

    print(over_seq)

    output_np_to_file(over_seq, os.path.join(video, ".."), "over_seq")
    output_np_to_file(elbow_seq, os.path.join(video, ".."), "elbow_seq")

if __name__ == '__main__':
    main()