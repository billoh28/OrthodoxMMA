import sys, os
sys.path.insert(1, os.getcwd() + '/../')
from Body_Landmarks import Body_Landmarks


def test_distance_between_landmarks_diagonal():
    bl = set_up()
    assert (bl.distance_between_landmarks(0,1)) == 5

def test_distance_between_landmarks_horizontal():
    bl = set_up()
    assert (bl.distance_between_landmarks(1,2)) == 3

def test_distance_between_landmarks_vertical():
    bl = set_up()
    assert (bl.distance_between_landmarks(0,2)) == 4

def test_distance_between_landmark_and_point_diagonal():
    bl = set_up()
    assert (bl.distance_between_landmark_and_point(0,[9,16])) == 17

def test_distance_between_landmark_and_point_verticle():
    bl = set_up()
    assert (bl.distance_between_landmark_and_point(1,[4,6])) == 1

def test_distance_between_landmark_and_point_horizonal():
    bl = set_up()
    assert (bl.distance_between_landmark_and_point(2,[9,5])) == 8

def test_angle_between_landmarks_right_angle():
    bl = set_up()
    assert (bl.angle_between_landmarks(0,2,1) == 90)

def test_angle_between_landmarks_acute():
    bl = set_up()
    assert (bl.angle_between_landmarks(0,1,2) < 90)

def test_slope_1():
    bl = set_up()
    assert (bl.slope(0,1) == 4/3)

def test_slope_2():
    bl = set_up()
    assert (bl.slope(1,2) == 0)

def test_midpoint_1():
    bl = set_up()
    assert (bl.midpoint(0,1) == (2.5,3))

def test_midpoint_2():
    bl = set_up()
    assert (bl.midpoint(0,2) == (1,3))

def test_get_X_and_Y_coor_1():
    bl = set_up()
    assert bl.get_X_and_Y_coor(1) == (4,5)

def test_get_X_and_Y_coor_2():
    bl = set_up()
    assert bl.get_X_and_Y_coor(2) == (1,5)


def set_up():
    landmarks =[]
    landmarks.append(Landmark1())
    landmarks.append(Landmark2())
    landmarks.append(Landmark3())
    bl = Body_Landmarks(landmarks,1,1,norm_cond=False)
    return bl


class Landmark1(object):
    def __init__(self):
        self.x = 1
        self.y = 1
        self.visibility = 1

class Landmark2(object):
    def __init__(self):
        self.x = 4
        self.y = 5
        self.visibility = 1

class Landmark3(object):
    def __init__(self):
        self.x = 1
        self.y = 5
        self.visibility = 1

