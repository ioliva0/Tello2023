from djitellopy import tello, Tello

from threading import Thread
from time import time, sleep
from random import randint

from numpy import zeros
import cv2

from json import load

balloons = []

with open("Calibration/Calibration.json", "r") as calibration_file:
    calibration = load(calibration_file)
    calibration_file.close()
distortion_coefficients = calibration["Distortion Coefficients"]
camera_matrix = calibration["Camera Matrix"]


display_downscale = 150/720

balloon_data = {}

colors = {
    "red" : ((161, 0, 43), (255, 72, 113)),
    "pink" : ((182, 121, 157), (212, 173, 211)),
    "orange" : ((182, 55, 0), (255, 147, 62)),
    "yellow" : ((169, 87, 0), (236, 255, 15)),
    "dark_green" : ((17, 117, 0), (43, 169, 69)),
    "light_green" : ((88, 174, 74), (116, 255, 170)),
    "purple" : ((102, 78, 150), (186, 122, 203)),
    "dark_blue" : ((14, 74, 117), (59, 115, 171)),
    "light_blue" : ((67, 132, 129), (99, 153, 175))
}

def create_color_dict():
    dict = {}
    for color in colors:
        dict[color] = 0
    return dict

blank_image = zeros([150, 200])


for i, color in enumerate(colors):
    cv2.namedWindow(color, cv2.WINDOW_NORMAL)
    cv2.imshow(color, blank_image)
    cv2.moveWindow(color, 200 * (i % 3), 170 * int(i / 3))

main_window = "stream"
cv2.namedWindow(main_window, cv2.WINDOW_NORMAL)
cv2.imshow(main_window, blank_image)
cv2.moveWindow(main_window, 200, 510)

"""
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

tag_size_in = 7
#side an int 1 or -1 depending on which side ur looking at
#1 is right, -1 is left
def sweep(tello: Tello, start: tuple, direction: tuple, speed: int, side : int):
    movement = Thread(target=tello.go_xyz_speed, args=[*direction, speed])
    
    movement.start()
    start_time = time()

    while movement.is_alive():
        tello_image = tello.get_frame_read().frame

        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        masks = {}

        for color in colors:

            mask = cv2.inRange(tello_image, *colors[color])
            mask = cv2.dilate(mask, None, iterations=5)
            mask = cv2.erode(mask, None, iterations=5)

            masks[color] = mask

            mask_display = cv2.resize(mask, (200, 150))

            cv2.imshow(color, mask_display)
            """
            contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                
                #downscales x,y,w,h to show on smaller display image
                (x, y, w, h) = tuple(int(dim / display_downscale) for dim in (x, y, w, h))

                cv2.rectangle(mask_display, (x, y), (x+w, y+h), (0,0,0))
            """
        
        # Detect ArUco markers in the image
        corners, ids, _ = arucoDetector.detectMarkers(true_image)

        if ids is None:
            continue

        for i, id in enumerate(ids):
            rot_vec , trans_vec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, tag_size_in, camera_matrix, distortion_coefficients)
            print("ID: " + id)
            print("Rotation vector: " + str(rot_vec))
            print("Translation vector: " + str(trans_vec))

            if balloon_data[id] is None:
                balloon_data[id] = {
                    "Colors" : [],
                    "Color_Confidences" : create_color_dict(),
                    "Times" : [],
                    "Translation_Vectors" : [],
                    "Rotation_Vectors" : [],
                }
            balloon_data[id]["Times"].append(time() - start_time)
            balloon_data[id]["Translation_Vectors"].append[trans_vec]
            balloon_data[id]["Rotation_Vectors"].append[rot_vec]

            x_vals = []
            y_vals = []
            for corner in corners[i][0]:
                x_vals.append(corner[0])
                y_vals.append(corner[1])

            avg_x = sum(x_vals) / len(x_vals)
            avg_y = sum(y_vals) / len(y_vals)

            range_x = max(x_vals) - min(x_vals)
            range_y = max(y_vals) - min(y_vals)



            confidences = create_color_dict()

            num_samples = 1000
            for sample in range(num_samples):
                sample_x = randint(avg_x - range_x, avg_x + range_x)
                sample_y = randint(avg_y - range_y, avg_y + range_y)

                for color in masks:
                    confidences[color] += masks[color][sample_y][sample_x]
                    balloon_data[id]["Color_Confidences"][color] += confidences[color]                    
    
    sweep_balloons = []
    
    total_time = time() - start_time

    for id in balloon_data:
        balloon = {}
        balloon["ID"] = id


        max_color = ""
        max_confidence = 0
        for color in balloon_data[id]["Color_Confidences"]:
            if balloon_data[id]["Color_Confidences"][color] > max_confidence:
                max_confidence = balloon_data[id]["Color_Confidences"][color]
                max_color = color
        
        balloon["Color"] = color
        
        distances = [distance[:2] for distance in distances]

        for i, time in enumerate(balloon_data[id]["Times"]):
            distance_center = tuple((time / total_time) * coord for coord in  direction)
            trans_vec = balloon_data[id]["Translation_Vectors"][i][:2]
            distance = tuple(side * coord + distance_center[coordInd] for coordInd, coord in enumerate(trans_vec))
            distances.append(distance)
        
        avg_distance = ()

        for distance in distances:
            for coordInd in range(len(distance)):
                avg_distance[coordInd] += distance[coordInd] / len(distances)
    
        balloon["Distance"] = avg_distance

        sweep_balloons.append(balloon)

    """
    [
        {
            ID : 1
            Color : Red
            Position(ft) : (x, y)
        }
    ]
    """

    balloons.append[sweep_balloons]

tello = Tello()

tello.connect()
tello.streamon()

tello.takeoff()

try:
    tello.move_forward(381)
    tello.rotate_counter_clockwise(90)

    sweep(tello, (-381, 0, 0), (381, 0, 0), 50, -1)
    sweep(tello, (0, 0, 0), (381, 0, 0), 50, -1)
    tello.rotate_counter_clockwise(180)
    sweep(tello, (381, 0, 0), (-381, 0, 0), 50, 1)
    sweep(tello, (0, 0, 0), (-381, 0, 0), 50, 1)

    tello.move_right(381)
    tello.rotate_counter_clockwise(90)

    target_tag = 1
    target_color = "red"
    for balloon in balloons:
        if balloon["ID"] == target_tag and balloon["Color"] == target_color:
            tello.move_right(balloon["Distance"][0])
            tello.move_forward(balloon("Distance")[1])
            tello.move_back(50)
            break
            
    tello.streamoff()
    tello.land()
except Exception as e:
    tello.streamoff()
    tello.land()
    raise e