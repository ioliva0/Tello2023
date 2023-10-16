from djitellopy import tello, Tello
import cv2 
import os
import numpy as np

tello = Tello()

tello.connect()

tello.streamon()


window = "stream"

#starting_image = cv2.imread("/Users/jwang/Tello/Tello2023/picture.png")
#cv2.imshow(window, starting_image)

while True:
    try:
        tello_image = tello.get_frame_read().frame
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2GRAY)

        """
        ## max contrast 
        # read the input image
        # changed from 'frame2' to frame
        vid = cv2.imread('frame')
        """

        # define the alpha and beta
        contrast = 17 # Contrast control (0~127)
        brightness = 1 # Brightness control (0~100)

        # call convertScaleAbs function
        scaleAbs = cv2.convertScaleAbs(true_image, contrast, brightness)

        # display the output image
        cv2.imshow('adjusted', scaleAbs)

        ## 28x28
        #number_arr = np.asarray(tello_image) 

        img_resized = cv2.resize(scaleAbs, (28,28))

        cv2.imshow(window, img_resized)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        tello.streamoff()            
        print("terminating...")
        break

