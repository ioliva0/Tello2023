if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import Consts
tello = Consts.tello
import Config
import Telemetry

from numpy import zeros
import time

import cv2

def initialize_cv2():
    #starter image to initialize every window with
    blank_image = zeros([150, 200])

    #create a window, placed correctly in a 3x3 grid, for every color
    #these will be used to display the color masks
    for i, color in enumerate(Consts.colors):
        cv2.namedWindow(color, cv2.WINDOW_NORMAL)
        cv2.imshow(color, blank_image)
        cv2.moveWindow(color, 200 * (i % 3), 170 * int(i / 3))

    #create a primary window and move it next to the mask windows
    cv2.namedWindow(Consts.main_window, cv2.WINDOW_NORMAL)
    cv2.imshow(Consts.main_window, blank_image)
    cv2.moveWindow(Consts.main_window, 200, 510)

    #wait until windows load and pray that the user figures out how to use cv2
    print("Waiting for cv2 to load...")
    print("once cv2 loads, click to focus on any cv2 window")
    print("then press any key to continue")
    cv2.waitKey(0)
    

    Consts.tello_image = Consts.tello.get_frame_read().frame
    Telemetry.show_stream()

    print("cv2 loading complete (hopefully?)")

def initialize_detector():
    from cv2 import aruco
    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    arucoParams = aruco.DetectorParameters()
    return aruco.ArucoDetector(arucoDict, arucoParams)

def initialize_tello():

    tello.connect()
    tello.streamon()

    battery = tello.get_battery()
    print("\n########################################\n")
    print(str(battery) + "% Battery")
    print("\n########################################\n")
    if battery < 30:
        print("WARNING: LOW BATTERY")
        print("Strange errors may occur\n\n")

    #for some reason, the first image taken is always shown as black even if it contains info
    #so we take one frame and discard it here
    Consts.tello.get_frame_read()

def takeoff():
    if Config.takeoff:
        tello.takeoff()
        time.sleep(1)
        tello.move_up(40)