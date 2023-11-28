if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import time

from djitellopy import Tello
import cv2

import Data_Parser
import Determiner
import Consts
import Config
tello = Consts.tello

def step(step_size: int):

    Consts.current_y += (Consts.current_dir * step_size)
    print("field Y: " + str(Consts.current_y))

    if not Config.true_movement:
        time.sleep(0.05)
        return

    #move to next step alongside line
    tello.move_left(step_size)

def sweep(length: int = Consts.size, step_size: int =20):
    dist_remain = length

    while dist_remain > step_size:

        step(step_size)
        dist_remain -= step_size

        #get the current frame (BGR) from the tello video stream
        tello_image = tello.get_frame_read().frame
        #convert the current frame to RGB
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        #downscale and display the RGB image
        true_image_display = cv2.resize(true_image, [200, 150])
        cv2.imshow(Consts.main_window, true_image_display)
        print(true_image_display[0][0])

        #dict of images (numpy arrays) to be treated as booleans at each pixel
        #indexed by color
        #white ? black = color detected ? color not detected
        masks = {}

        for color in Consts.colors:
            """
            create a mask for every color, then fill arbitrary holes
            NOTE: may be better to just downscale the image at the beginning
            I'm still a little scared of antialiasing problems
            """
            mask = cv2.inRange(tello_image, *Consts.colors[color])
            mask = cv2.dilate(mask, None, iterations=5)
            mask = cv2.erode(mask, None, iterations=5)

            #add masks to dictionary
            masks[color] = mask

            #downscale and show each mask in its respective color window
            mask_display = cv2.resize(mask, [200, 150])
            cv2.imshow(color, mask_display)
        
        # Detect ArUco markers in the image
        corners, ids, _ = Consts.arucoDetector.detectMarkers(true_image)

        #stop if image is outputted but no balloons are detected
        if ids is None:
            continue
        
        for id in ids:
            Data_Parser.get_balloon_data(id, corners[id][0], masks)

    if dist_remain > 20:
        step(dist_remain)

    for id in Consts.balloon_data:
        Determiner.determine_balloon(id)