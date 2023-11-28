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
import Initializer
import Telemetry
tello = Consts.tello

arucoDetector = Initializer.initialize_detector()

def step(step_size: int):

    Consts.current_y += (Consts.current_dir * step_size)
    print("field Y: " + str(Consts.current_y))

    if not Config.true_movement:
        time.sleep(0.01)
        return

    #move to next step alongside line
    tello.move_left(step_size)

def sweep(length: int = Consts.size, step_size: int =40):
    dist_remain = length

    while dist_remain > step_size:

        step(step_size)
        dist_remain -= step_size

        #get the current frame (BGR) from the tello video stream
        Consts.tello_image = tello.get_frame_read().frame
        #convert the current frame to RGB

        for color in Consts.colors:
            """
            create a mask for every color, then fill arbitrary holes
            NOTE: may be better to just downscale the image at the beginning
            I'm still a little scared of antialiasing problems
            """
            mask = cv2.inRange(Consts.tello_image, *Consts.colors[color])
            mask = cv2.dilate(mask, None, iterations=5)
            mask = cv2.erode(mask, None, iterations=5)

            #add masks to dictionary
            Consts.masks[color] = mask
        
        Telemetry.show_all_images()

        # Detect ArUco markers in the image
        corners, ids, _ = arucoDetector.detectMarkers(Consts.tello_image)

        #stop if image is outputted but no balloons are detected
        if ids is None:
            continue
        
        ids = [id[0] for id in ids]

        for i, id in enumerate(ids):
            print(id)
            print(corners)
            Data_Parser.get_balloon_data(id, corners[i][0], Consts.masks)

    if dist_remain > 20:
        step(dist_remain)