import numpy
import cv2
from djitellopy import Tello

from math import cos, sin
import Consts

from Load_Handler import load_calibration

#https://stackoverflow.com/questions/75750177/solve-pnp-or-estimate-pose-single-markers-which-is-better
def estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    marker_points = numpy.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=numpy.float32)
    
    success, rotation_vector, translation_vector = cv2.solvePnP(marker_points, corners, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)

    translation_vector = [int(pos[0] * 10) / 10 for pos in translation_vector]
    translation_vector = (translation_vector[0], translation_vector[2])

    rotation_vector = [int(angle[0] * 10) / 10 for angle in rotation_vector]
    rotation = rotation_vector[2]

    return rotation, translation_vector

def find_balloon_center(translation_vector, rotation):
    x_offset = sin(rotation) * Consts.balloon_radius_in
    z_offset = cos(rotation) * Consts.balloon_radius_in

    x = int((translation_vector[0] + x_offset) * 10) / 10
    z = int((translation_vector[1] + z_offset) * 10) / 10

    return x, z

def draw_text(image, text, org):
    image = cv2.putText(image, str(text), org, cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 8, cv2.LINE_AA)
    return cv2.putText(image, str(text), org, cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3, cv2.LINE_AA)

# Create a Tello instance
tello = Tello()

# Connect to the Tello and start the video stream
tello.connect()
tello.streamon()

battery = tello.get_battery()
print("\n########################################\n")
print(str(battery) + "% Battery")
print("\n########################################\n")

# Create a window for the video stream
window = "Tello Stream"
cv2.namedWindow(window)

calibration = load_calibration()

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

while cv2.waitKey(200) != ord("q"):
    try:
        tello.send_keepalive()
        
        tello_image = tello.get_frame_read().frame
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers in the image
        corners, ids, rejected = arucoDetector.detectMarkers(true_image)

        # If ArUco markers are detected, print their IDs
        if ids is not None:
            for i in range(len(ids)):
                aruco_id = ids[i][0]
                cv2.aruco.drawDetectedMarkers(true_image, corners, ids)

                rot, trans_vec = estimatePoseSingleMarkers(corners[i][0], 3, *calibration)

                true_image = draw_text(true_image, trans_vec, (50, 200 + 100 * i))
                true_image = draw_text(true_image, rot, (400, 200 + 100 * i))
                true_image = draw_text(true_image, find_balloon_center(trans_vec, rot), (600, 200 + 100 * i))

        cv2.imshow(window, true_image)
    except KeyboardInterrupt:
        break

print("Terminating...")
tello.streamoff()
