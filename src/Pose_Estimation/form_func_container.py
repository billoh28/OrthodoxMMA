'''
This program has been deprecated by our jab_classifier program. 
'''

''' Program containing functions for checking form of strikes on frames contained within a Frame_Collection object.
The functions with this program should only be called from outside the program in production. '''

# Function for checking the stance of the user
# Takes a Frame_Collection  object as input
def stance_check(fc, ignore_left=False, ignore_right=False):
    arm_angle_satisfied_counter = 0
    #hand_to_nose_satisfied_counter = 0
    elbows_tucked_satisfied_counter = 0

    #Given all the frames, get an average performance
    for frame in fc.frame_collection:
        #Shoulder and hips
        # left_mid_body = frame.midpoint(11, 23)
        # right_mid_body = frame.midpoint(12, 24)
        if not ignore_left and not ignore_right:
            # Check that angle from shoulder, elbow to wrist is at least an accute angle
            if (frame.angle_between_landmarks(12, 14, 16) < 50) & (frame.angle_between_landmarks(15, 13, 11) < 50):
                arm_angle_satisfied_counter += 1

            '''
            # Check that the wrists are close to the head
            if ((frame.distance_between_landmarks(0, 15) < 140) & (frame.distance_between_landmarks(0, 16) < 140)):
                hand_to_nose_satisfied_counter += 1
            '''

            # Check that the elbow are close to the midpoint of the body
            # Check the distance from the shoulder to hip
            # Check the distance from shoulder to elbow
            # Calculate that the difference of the two lengths are at a ratio of 0.3 - 0.7
            left_shoulder_to_hip = frame.distance_between_landmarks(12, 24) 
            right_shoulder_to_hip = frame.distance_between_landmarks(11, 23)
            left_shoulder_to_elbow = frame.distance_between_landmarks(12, 14) 
            right_shoulder_to_elbow = frame.distance_between_landmarks(11, 13)

            if ((left_shoulder_to_elbow / left_shoulder_to_hip) < 0.3) & ((right_shoulder_to_elbow / right_shoulder_to_hip) < 0.3):
                elbows_tucked_satisfied_counter -= 1

            # if ((frame.distance_between_landmark_and_point(13, left_mid_body) < 120) & (frame.distance_between_landmark_and_point(14, right_mid_body) < 120)):
            #     elbows_tucked_satisfied_counter += 1
            

            # Check that arms are close to body i.e. angles between elbow, shoulder and hip
            if (frame.angle_between_landmarks(13, 11, 23) < 50) & (frame.angle_between_landmarks(14, 12, 24) < 50):
                elbows_tucked_satisfied_counter += 1


    # 80 percent satisfaction rate
    if (arm_angle_satisfied_counter / len(fc.frame_collection))*100 > 70:
        print("Stance is satisfied")
    else:
        print("Close the angle on elbow")
    
    #if (hand_to_nose_satisfied_counter / len(fc.frame_collection))*100 > 70:
        #print("Stance is satisfied")
    #else:
        #print("Try getting your hands closer to your head")

    if (elbows_tucked_satisfied_counter / len(fc.frame_collection))*100 > 70:
        print("Stance is satisfied")
    else:
        print("Try getting your elbows closer to your body")
    
    print(elbows_tucked_satisfied_counter / len(fc.frame_collection)*100)

#Function for live feed of stance recommendations
def live_stance_check(frame, ignore_left=False, ignore_right=False):
    arm_angle_satisfied_counter = 0
    #hand_to_nose_satisfied_counter = 0
    elbows_tucked_satisfied_counter = 0

    # Shoulder and hips
    # left_mid_body = frame.midpoint(11, 23)
    # right_mid_body = frame.midpoint(12, 24)
    if not ignore_left and not ignore_right:
        # Check that angle from shoulder, elbow to wrist is at least an accute angle
        if (frame.angle_between_landmarks(12, 14, 16) < 50) & (frame.angle_between_landmarks(15, 13, 11) < 50):
            arm_angle_satisfied_counter += 1

        '''
        # Check that the wrists are close to the head
        if ((frame.distance_between_landmarks(0, 15) < 140) & (frame.distance_between_landmarks(0, 16) < 140)):
            hand_to_nose_satisfied_counter += 1
        '''

        # Check that the elbow are close to the midpoint of the body
        # Check the distance from the shoulder to hip
        # Check the distance from shoulder to elbow
        # Calculate that the difference of the two lengths are at a ratio of 0.3 - 0.7
        left_shoulder_to_hip = frame.distance_between_landmarks(12, 24) 
        right_shoulder_to_hip = frame.distance_between_landmarks(11, 23)
        left_shoulder_to_elbow = frame.distance_between_landmarks(12, 14) 
        right_shoulder_to_elbow = frame.distance_between_landmarks(11, 13)

        if ((left_shoulder_to_elbow / left_shoulder_to_hip) < 0.3) or ((right_shoulder_to_elbow / right_shoulder_to_hip) < 0.3):
            print("Elbows are too high, lower closer to sides")
        else:
            print("Satisfied")

        # Check that arms are close to body i.e. angles between elbow, shoulder and hip
        if (frame.angle_between_landmarks(13, 11, 23) > 50) or (frame.angle_between_landmarks(14, 12, 24) > 50):
            print("Angle between elbow and hip too high, please reduce")
        else:
            print("Satisfied")

        # Check that the arms bent towards the face
        if (frame.angle_between_landmarks(11,13,15) > 50 or frame.angle_between_landmarks(12,14,16) > 50):
            print("Arms too straight, try putting hands closer to face")
        else:
            print("Satisfied")


# Function to check the form of a jab contained within a Frame_Collection object
def jab_check(fc, orient=0): # orient=0 is for orthodox and orient=1 is for southpaw

    '''
    Only concerned about upper body to start.
    1. Hands up, elbows in. Keep power arm up and covering chin.
    2. Extend front glove straight, towards opponent. Move only the front arm, no shifting weight forwards or backwards.
    3. When extending outwards, rotate the front arm so that the punch lands with the palm facing down, and the shoulder covering the chin.
    '''

    # Got to find start of jab, find end of jab, repeat till end of frames

    face_protection_checker = 0
    body_protection_checker = 0
    face_protected_by_shoulder_checker = 0
    #Counts the number of stikes
    no_of_strikes = 0
    #In strike condition
    in_strike_action_cond = False
    #For checking that the shoulder gets higher while in striking motion
    shoulder_level = 0
    shoulder_to_nose_distance = 0
    #Fully extended jab arm
    full_extend_strike = False
    full_extend_strike_checker = 0

    for frame in fc.frame_collection[10:-10]:

        left_shoulder_to_hip = frame.distance_between_landmarks(12, 24) 
        right_shoulder_to_hip = frame.distance_between_landmarks(11, 23)
        left_shoulder_to_elbow = frame.distance_between_landmarks(12, 14) 
        right_shoulder_to_elbow = frame.distance_between_landmarks(11, 13)

        # Check the unused arm is always protecting the face
        # Check the unused arm is always protecting the body
        if (left_shoulder_to_elbow / left_shoulder_to_hip) < 0.3:
            body_protection_checker += 1
        
        # Check the unused arm is always protecting the face
        if (frame.angle_between_landmarks(11,13,15) > 50 or frame.angle_between_landmarks(13, 11, 23) > 50):
            face_protection_checker += 1

        # if arm elbow angle is stright then has started
        # This is when the strike has commenced
        if (frame.angle_between_landmarks(12,14,16) > 50):
            if in_strike_action_cond == False:
                no_of_strikes += 1
                in_strike_action_cond = True
                shoulder_level = frame.get_X_and_Y_coor(12)[1] #Y-Coordinates of the striking shoulder
                shoulder_to_nose_distance = frame.distance_between_landmarks(0,12) #Distance from shoulder to nose
            
            # Check if the face is protected by shoulder by seeing is the shoulder has risen the start of the strike
            # If not the checker will increase
            if (frame.get_X_and_Y_coor(12)[1] <= shoulder_level) & (frame.distance_between_landmarks(0,12) <= shoulder_to_nose_distance):
                face_protected_by_shoulder_checker += 1

            # Make sure the arm is, at one stange during the jab strike, fully extended
            if (frame.angle_between_landmarks(12,14,16) > 150) and full_extend_strike == False:
                full_extend_strike_checker += 1
                full_extend_strike = True

        else:
            full_extend_strike = False
            in_strike_action_cond = False

    print("Number of Strikes: {}".format(no_of_strikes))
    print("Number of fully extended strikes: {}".format(full_extend_strike_checker))
    print("Number of Frames Body was not protected: {}".format(body_protection_checker))
    print("Number of Frames Face was not protected: {}".format(face_protection_checker))
    print("Number of Frames Face was not protected by shoulder while in strike motion: {}".format(face_protected_by_shoulder_checker))
    

        