from djitellopy import tello, Tello

from threading import Thread
from time import time, sleep

from numpy import zeros
import cv2

display_downscale = 150/720

balloons = {}

colors = {
    "red" : ((0,0,0),(0,0,0)),
    "pink" : ((0,0,0),(0,0,0)),
    "orange" : ((0,0,0),(0,0,0)),
    "yellow" : ((0,0,0),(0,0,0)),
    "dark_green" : ((0,0,0),(0,0,0)),
    "light_green" : ((0,0,0),(0,0,0)),
    "purple" : ((0,0,0),(0,0,0)),
    "dark_blue" : ((0,0,0),(0,0,0)),
    "light_blue" : ((0,0,0),(0,0,0))
}

blank_image_display = zeros([150, 200])
"""
blank_image = zeros([720, 960])


for i, color in enumerate(colors):
    cv2.namedWindow(color, cv2.WINDOW_NORMAL)
    cv2.imshow(color, blank_image_display)
    cv2.moveWindow(color, 200 * (i % 3), 170 * int(i / 3))
"""
main_window = "stream"
cv2.namedWindow(main_window, cv2.WINDOW_NORMAL)
cv2.imshow(main_window, blank_image_display)
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

def sweep(tello: Tello, direction: tuple, speed: int):
    timer = Thread(target=tello.go_xyz_speed, args=[*direction, speed])
    
    timer.start()

    while timer.is_alive():
        tello_image = tello.get_frame_read().frame

        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        """
        for color in colors:
            mask = cv2.inRange(tello_image, *colors[color])
            mask = cv2.dilate(mask, None, iterations=5)
            mask = cv2.erode(mask, None, iterations=5)

            mask_display = cv2.resize(mask, (200, 150))

            cv2.imshow(color, mask_display)

            contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                
                #downscales x,y,w,h to show on smaller display image
                (x, y, w, h) = tuple(int(dim / display_downscale) for dim in (x, y, w, h))

                cv2.rectangle(mask_display, (x, y), (x+w, y+h), (0,0,0))
        """

        # Detect ArUco markers in the image
        corners, ids, rejected = arucoDetector.detectMarkers(true_image)


        cv2.imshow(main_window, true_image)
        cv2.waitKey(1)
