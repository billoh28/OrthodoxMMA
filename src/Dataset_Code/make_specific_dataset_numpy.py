'''
This program is similar to previous dataset programs, except it takes datapoints as input and excludes those which are not included in the input
'''

import sys, os, random
import numpy as np
from tqdm import tqdm

# Custom library
from make_dataset_tsv import make_dataset



def main():
    # This program is to make a custom dataset from specific local data
    # e.g. python make_dataset_numpy.py "C:\Users\ohanl\Documents\CA400-Project\CA400-videos\Hands_up" hands 11 12 13 14 23 24 25 26 27 28 29 30 31 32

    # Take file location of video for datatset off of commmandline
    VIDEO_LOCATION = sys.argv[1]

    # Take name off commandline
    NAME = sys.argv[2]

    important_points = []
    if len(sys.argv) > 3: # Important points provided
        important_points = [int(n) for n in sys.argv[3:]]

        # Abstract data from videos and saved returned list
        result = make_dataset(VIDEO_LOCATION)

        # Send frames to numpy array handler
        output_np_to_file(result[1:], VIDEO_LOCATION, NAME, important_points) # ignore first element in result as it is csv headers

if __name__ == '__main__':
    main()