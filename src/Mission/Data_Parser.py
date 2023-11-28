import cv2

import Colors

from random import randint

import Consts

def get_balloon_data(id, corners, masks):
    #use camera calibration and aruco tag info to get drone's distance to tag
    #INCHES, not centimeters
    rot_vec , trans_vec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, Consts.tag_size_in, *Consts.calibration)
    print("ID: " + id)
    print("Translation vector: " + str(trans_vec))

    """
    initialize dictionary and add to balloon_data 
    this includes tag ID and all non-deterministic information about balloon
    NOTE: a fundamental flaw in our code is that it assumes it's unconfident
    and will not ever use balloon color to determine balloon type
    this means that multiple balloons with the same tag will be mixed up
    and assumed to be the same tag
    """
    if Consts.balloon_data[id] is None:
        Consts.balloon_data[id] = {
            "Color_Confidences" : Colors.create_color_dict(),
            "Y_Values" : [],
            "Translation_Vectors" : []
        }
    #add current information to balloon data
    #this is not yet processed
    Consts.balloon_data[id]["Y_Values"].append[Consts.current_y]
    Consts.balloon_data[id]["Translation_Vectors"].append[trans_vec]

    #get the center and length of the aruco tag's bounding box
    x_vals = []
    y_vals = []
    for corner in corners:
        x_vals.append(corner[0])
        y_vals.append(corner[1])

    avg_x = sum(x_vals) / len(x_vals)
    avg_y = sum(y_vals) / len(y_vals)

    range_x = max(x_vals) - min(x_vals)
    range_y = max(y_vals) - min(y_vals)

    #create a "confidence score" based on how many random samples
    #within double the aruco tag's bounding box (the estimated bounding box of the balloon)
    #and add each confidence to a dictionary, indexed by the color's name
    confidences = Colors.create_color_dict()

    num_samples = 1000
    for sample in range(num_samples):
        sample_x = randint(avg_x - range_x, avg_x + range_x)
        sample_y = randint(avg_y - range_y, avg_y + range_y)

        #adds the pixel value of the mask at the sample to the confidence score
        #this works becuase positive detections are white (255) and negative detections are black (0)
        for color in masks:
            confidences[color] += masks[color][sample_y][sample_x]
            Consts.balloon_data[id]["Color_Confidences"][color] += confidences[color]