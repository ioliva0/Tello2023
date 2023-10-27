from djitellopy import tello, Tello
import cv2
from imutils import resize
from random import randint

tello = Tello()

tello.connect()

tello.streamon()

tello.takeoff()

window = "stream"

while True:
    try:
        tello.send_keepalive()

        tello_image = tello.get_frame_read().frame
        tello_image = resize(tello_image, width=600)

        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        blue = cv2.inRange(tello_image, (0, 0, 100), (90, 140, 255))
        green = cv2.inRange(tello_image, (0, 110, 0), (90, 255, 170))
        red = cv2.inRange(tello_image, (110, 0, 0), (255, 60, 120))

        cv2.imshow("red", red)
        cv2.imshow("green", green)
        cv2.imshow("blue", blue)
        
        cv2.imshow(window, true_image)
        cv2.waitKey(1)

        thresh = 100
        samples = 1000


        redSamples = 0
        greenSamples = 0
        blueSamples = 0
        for sample in range(samples):
            x = randint(0, 599)
            y = randint(0, 336)

            redSamples += red[y][x] / 255
            greenSamples += green[y][x] / 255
            blueSamples += blue[y][x] / 255

        maxSamples = max(redSamples, greenSamples, blueSamples)
        if maxSamples >= thresh:
            if maxSamples == redSamples:
                color = "red"
            elif maxSamples == greenSamples:
                color = "green"
            else:
                color = "blue"
        else:
            color = "none"
        
        print(color, end="   \r")

            

    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("terminating...")
        break