if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import Consts
tello = Consts.tello
import Config

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

    frame = Consts.tello.get_frame_read().frame
    frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), [150, 200])

    cv2.namedWindow(Consts.main_window, cv2.WINDOW_NORMAL)
    cv2.imshow(Consts.main_window, frame)
    cv2.moveWindow(Consts.main_window, 200, 510)

    #wait until windows load and pray that the user figures out how to use cv2
    print("Waiting for cv2 to load...")
    print("once cv2 loads, click to focus on any cv2 window")
    print("then press any key to continue")
    cv2.waitKey(0)
    print("cv2 loading complete (hopefully?)")

def initialize_tello():

    tello.connect()
    tello.streamon()

    print(str(tello.get_battery()) + "% Battery")


def takeoff():
    if Config.takeoff:
        tello.takeoff()
        time.sleep(1)
        tello.move_up(40)