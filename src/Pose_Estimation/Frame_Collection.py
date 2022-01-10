from Body_Landmarks import Body_Landmarks

class Frame_Collection(object):

    def __init__(self, technique):
        self.technique = technique
        self.frame_collection = []
        # self.video_dimensions = [width, height] # Video dimensions used later on for normalisation

    def add(self, frame):
        self.frame_collection.append(frame)

    def __iter__(self):
        yield from self.frame_collection

