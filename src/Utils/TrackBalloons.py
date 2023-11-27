from djitellopy import tello, Tello

from threading import Thread
import time
from random import randint

from numpy import zeros
import cv2

from json import load

from math import pi

with open("Calibration/Calibration.json", "r") as calibration_file:
    calibration = load(calibration_file)
    calibration_file.close()
distortion_coefficients = calibration["Distortion Coefficients"]
camera_matrix = calibration["Camera Matrix"]

target_color = input("Target color: ")
target_tag = input("Target ID: ")

display_downscale = 150/720

balloon_data = {}

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

print("Waiting for cv2 to load...")
print("Press any key in a python window once they pop up to continue")
cv2.waitKey(0)
print("cv2 loading complete (hopefully?)")

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

tag_size_in = 3
#side an int 1 or -1 depending on which side ur looking at
#1 is right, -1 is left
def sweep(tello: Tello, direction: tuple, speed: int, side : int):
    
    movement = Thread(target=tello.go_xyz_speed, args=[-direction[1],direction[0],direction[2], speed])
    movement.daemon = True
    movement.start()
    
    start_time = time.time()

    while abs(tello.get_speed_x() + tello.get_speed_y()) > 1:
        tello_image = tello.get_frame_read().frame

        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        true_image_display = cv2.resize(true_image, (200, 150))

        cv2.imshow(main_window, true_image_display)

        masks = {}

        for color in colors:

            mask = cv2.inRange(tello_image, *colors[color])
            mask = cv2.dilate(mask, None, iterations=5)
            mask = cv2.erode(mask, None, iterations=5)

            masks[color] = mask

            mask_display = cv2.resize(mask, (200, 150))

            cv2.imshow(color, mask_display)
        
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
            balloon_data[id]["Times"].append(time.time() - start_time)
            balloon_data[id]["Translation_Vectors"].append(trans_vec)
            balloon_data[id]["Rotation_Vectors"].append(rot_vec)

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
    
    total_time = time.time() - start_time

    for id in balloon_data:
        balloon = {}
        balloon["ID"] = id


        max_color = ""
        max_confidence = 0
        for color in balloon_data[id]["Color_Confidences"]:
            if balloon_data[id]["Color_Confidences"][color] >= max_confidence:
                max_confidence = balloon_data[id]["Color_Confidences"][color]
                max_color = color
        
        balloon["Color"] = max_color
        
        distances = []
        distances = [distance[:2] for distance in distances]

        for i, curr_time in enumerate(balloon_data[id]["Times"]):
            distance_center = tuple((curr_time / total_time) * coord for coord in  direction)
            trans_vec = balloon_data[id]["Translation_Vectors"][i][:2]
            distance = tuple(coord + distance_center[coordInd] for coordInd, coord in enumerate(trans_vec))
            distances.append(distance)
        
        avg_distance = [0,0]

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

    #return sweep_balloons
    return []

def correct_pos(balloons, y, dir):
    for balloon in balloons:
        corrected_position = [0,0]
        corrected_position[0] = balloon["Position"][1] * dir
        corrected_position[1] = y + balloon["Position"][1] * dir

    return balloons


tello = Tello()

tello.connect()
tello.streamon()

tello.takeoff()

time.sleep(2)

tello.move_up(40)

y = 0
balloons = []
dir = None

size = 381
#381

try:
    tello.move_forward(size)
    tello.rotate_counter_clockwise(90)
    y = size
    dir = -1

    #sweep to the left, downwards from top
    sweep_balloons = sweep(tello, (size, 0, 0), 50, -1)
    balloons.extend(correct_pos(sweep_balloons, y, dir))
    y = 0

    sweep_balloons = sweep(tello, (size, 0, 0), 50, -1)
    balloons.extend(correct_pos(sweep_balloons, y, dir))
    tello.rotate_counter_clockwise(180)
    y = -size
    dir = 1

    #sweep to the right, upwards from bottom
    sweep_balloons = sweep(tello, (size, 0, 0), 50, 1)
    balloons.extend(correct_pos(sweep_balloons, y, dir))
    y = 0

    sweep_balloons = sweep(tello, (size, 0, 0), 50, 1)
    balloons.extend(correct_pos(sweep_balloons, y, dir))

    tello.go_xyz_speed(0,-size,0,50)
    tello.rotate_counter_clockwise(90)

    print(balloons)

    if len(balloons) > 0:
        for balloon in balloons:
            if balloon["ID"] == target_tag and balloon["Color"] == target_color:
                tello.move_right(balloon["Distance"][0])
                tello.move_forward(balloon["Distance"][1])
                tello.move_back(50)
                break
except Exception as e:
    tello.streamoff()
    tello.land()
    raise e

tello.streamoff()
tello.land()