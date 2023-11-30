if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import cv2

import Colors

from random import randint, choice

import Consts
import Geolocator

def get_random_sample_ring(midpoint, radius, upper_bound, ring_size = 1.5):
    if choice([True, False]):
        sample = randint(midpoint - int(radius / 2 * ring_size), midpoint - int(radius/2)) 
    else:
        sample = randint(midpoint + int(radius / 2), midpoint + int(radius / 2 * ring_size)) 

    #sample += randint(0, 1) * int(radius * 3/2)
    sample = int(max(min(sample, upper_bound - 1), 0))
    return sample

def get_balloon_data(id, corners, masks):
    #use camera calibration and aruco tag info to get drone's distance to center of balloon
    #INCHES, not centimeters
    trans_vec = Geolocator.find_balloon_center(corners)

    key = str(id)

    print("ID: " + key)
    #print("Translation vector: " + str(trans_vec))

    """
    initialize dictionary and add to balloon_data 
    this includes tag ID and all non-deterministic information about balloon
    NOTE: a fundamental flaw in our code is that it assumes it's unconfident
    and will never use balloon color to determine balloon type
    this means that multiple balloons with the same tag will be mixed up
    and assumed to be the same tag
    """
    if key not in Consts.balloon_data:
        Consts.balloon_data[key] = {
            "Color_Confidences" : Colors.create_color_dict(),
            "Hue_Scores" : [],
            "Y_Values" : [],
            "Translation_Vectors" : [],
            "Dir" : Consts.current_dir
        }
    #add current information to balloon data
    #this is not yet processed
    Consts.balloon_data[key]["Y_Values"].append(Consts.current_y)
    Consts.balloon_data[key]["Translation_Vectors"].append(trans_vec)
    
    hsv_image = cv2.cvtColor(Consts.tello_image, cv2.COLOR_BGR2HSV)

    #get the center and length of the aruco tag's bounding box
    x_vals = []
    y_vals = []
    for corner in corners:
        x_vals.append(corner[0])
        y_vals.append(corner[1])

    avg_x = int(sum(x_vals) / len(x_vals))
    avg_y = int(sum(y_vals) / len(y_vals))

    #redundant casting, but stops the "compiler" from complaining
    range_x = int(max(x_vals) - min(x_vals))
    range_y = int(max(y_vals) - min(y_vals))
    
    num_samples = 1000

    hsvs = []
    for sample in range(num_samples):
        
        #choose a random sample in a ring around the aruco tag, not including the tag itself
        sample_x = get_random_sample_ring(avg_x, range_x, 960)
        sample_y = get_random_sample_ring(avg_y, range_y, 720)

        #adds the pixel value of the mask at the sample to the confidence score
        #this works becuase positive detections are white (255) and negative detections are black (0)
        for color in masks:
            Consts.balloon_data[key]["Color_Confidences"][color] += int(masks[color][sample_y][sample_x] / 255)

        hsvs.append(hsv_image[sample_y][sample_x].tolist())

    total_weight = 0
    total_hue = 0
    for hsv in hsvs:
        weight = (hsv[1] + hsv[2])
        total_hue += hsv[0] * weight
        total_weight += weight

    hue_score = total_hue / total_weight

    Consts.balloon_data[key]["Hue_Scores"].append(hue_score)

    