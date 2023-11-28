import cv2
import Consts
from numpy import zeros

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
    print("cv2 loading complete (hopefully?)")