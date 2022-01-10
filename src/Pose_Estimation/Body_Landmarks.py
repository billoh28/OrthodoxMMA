import math

class Body_Landmarks(object):
    """Class to hold all 32 human pose landmarks for a particular frame"""
    def __init__(self, frame_landmarks, width, height, norm_cond=True):
        self.landmarks_names = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'LEFT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']
        self.landmarks = []

        for landmark in frame_landmarks:
            self.landmarks.append([landmark.x * width, landmark.y * height, landmark.visibility])

        # Normalise body landmarks after loading in
        if norm_cond:
            self.normalise()

    def __str__(self):
        output = ""
        i = 0
        for l in self.landmarks:
            output = output + "{:}: x = {:.2f}, y = {:.2f}, visibility = {:.2f}\n".format(self.landmarks_names[i], l[0], l[1], l[2])
            i += 1

        return output

    # Method for calculating the distance between two landmarks
    # Expects the landmarks to be given i the form of integerss
    def distance_between_landmarks(self, l_1, l_2):
        # Euclidean distance function
        # 0 == x & 1 == y
        return ((self.landmarks[l_1][0] - self.landmarks[l_2][0])**2 + (self.landmarks[l_1][1] - self.landmarks[l_2][1])**2)**(0.5)

    def distance_between_landmark_and_point(self, l_1, point):
        return ((self.landmarks[l_1][0] - point[0])**2 + (self.landmarks[l_1][1] - point[1])**2)**(0.5)

    def angle_between_landmarks(self, l_1, l_2, l_3):        
 
        a = self.distance_between_landmarks(l_1, l_2)
        b = self.distance_between_landmarks(l_2, l_3)
        c = self.distance_between_landmarks(l_1, l_3)

        angle = math.degrees(math.acos(((a**2) + (b**2) - (c**2))/(2 * a * b))) # Cosine rule

        return angle       

    def slope(self, l_1, l_2):
        return((self.landmarks[l_2][1] - self.landmarks[l_1][1]) / (self.landmarks[l_2][0] - self.landmarks[l_1][0]))

    def midpoint(self, l_1, l_2):
        # Returns the coordinates of the midpoints in a tuple
        return((self.landmarks[l_1][0] + self.landmarks[l_2][0]) / 2 , (self.landmarks[l_1][1] + self.landmarks[l_2][1]) / 2)

    def get_X_and_Y_coor(self, lm):
        return self.landmarks[lm][0], self.landmarks[lm][1]

    def normalise(self):
        # Normalise body landmarks based on a centre of the landmarks.
        # The landmarks taken from BlazePose are normalised on the width and height of the inputted video.
        # However, this is not ideal when predicting form over videos of different dimensions, as the body landmarks skew with the dimensions.
        # e.g. if the inputted data has a large width in respect to the height, then the landmarks will be stretched.
        # Therefore, must normalised based on a centre of the body landmarks predicted, as this should be the same regardless of video dimensions i.e. (0,0)
        # The centre we have chosen is the shoulders i.e. 11 and 12.

        # This normalisation code was adpated from https://google.github.io/mediapipe/solutions/pose_classification.html

        centre = self.midpoint(11, 12) # Midpoint of the shoulders
        max_dist = self.max_distance(centre)

        for i in range(len(self.landmarks)):
            # Take away centre, divide by max distance to scale and multiply by constant for easier viewing
            self.landmarks[i][0] = ((self.landmarks[i][0] - centre[0]) / max_dist) * 100
            self.landmarks[i][1] = ((self.landmarks[i][1] - centre[1]) / max_dist) * 100

        return


    def max_distance(self, centre):
        
        # Get landmark with maximum distance from new centre for normalisation
        import math
        max_dist = -math.inf

        for i in range(len(self.landmarks)):
            dist_from_centre = self.distance_between_landmark_and_point(i, centre)

            if dist_from_centre > max_dist:
                max_dist = dist_from_centre

        return max_dist