if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import Config

print("Initializing constants")
#print("if this happens more than once, something is SERIOUSLY wrong")

main_window = "stream"

import Load_Handler
calibration = Load_Handler.load_calibration()

tag_size_in = 3
balloon_radius_in = 4

#approximate size of HALF the field in cm, 12.5ft
size = 381 * Config.field_scale

colors = {
    "red" : ((161, 0, 43), (255, 72, 113)),
    "pink" : ((216, 131, 173), (255, 173, 209)),
    "orange" : ((138, 15, 0), (214, 65, 13)),
    "yellow" : ((167, 122, 0), (201, 161, 49)),
    "dark_green" : ((17, 117, 0), (43, 169, 69)),
    "light_green" : ((88, 174, 74), (116, 255, 170)),
    "purple" : ((55, 17, 74), (85, 66, 123)),
    "dark_blue" : ((14, 74, 117), (59, 115, 171)),
    "light_blue" : ((76, 117, 180), (158, 187, 225))
}

hues = {
    "red" : 125,
    "pink" : 128, #113
    "orange" : 112, #110
    "yellow" : 96, #86
    "dark_green" : 53,
    "light_green" : 77,
    "purple" : 160, #140
    "dark_blue" : 55, 
    "light_blue" : 48, #35
}


#dict of images (numpy arrays) to be treated as booleans at each pixel
#indexed by color
#white ? black = color detected ? color not detected
masks = {}

#dictionary of all unprocessed balloon data without conclusive results

"""
{
    "Color_Confidences" : {red: 9999, orange: 3524, yellow: 361, etc...}
    "Y_Values" : [381, 350]
    "Translation_Vectors" : [(50, 3, 5), (20, 20, -3)],
}

Color confidences are proportional to the number of positive samples on each color mask

Y values are the longitude of the drone at the time of each detection, IN CENTIMETERS

Translation vectors are the distance from the drone 
at the time of each detection to the given ArUCo tag, IN INCHES
"""
balloon_data = {}

"""
[
    {
        ID : 1
        Color : Red
        Position(ft) : (x, y)
    }
]
"""
balloons = []

current_y = 0
current_dir = 0

#get input from mission stage:

if Config.target:
    print("Valid colors: red, pink, orange, yellow, dark_green, light_green, purple, dark_blue, light_blue")
    target_color = input("Target color: ")
    target_tag = input("Target ID: ")

from djitellopy import Tello
tello = Tello()

tello_image = None