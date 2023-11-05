from djitellopy import tello, Tello
import cv2
from imutils import resize
from random import randint
from Utils.Hover import hover

tello = Tello()

tello.connect()

tello.streamon()

tello.takeoff()

window = "stream"

min_hsv = (70, 120, 50)
max_hsv = (100, 255, 255)

while True:
    try:

        tello_image = tello.get_frame_read().frame
        tello_image = resize(tello_image, width=600)

        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        blue = cv2.inRange(tello_image, (0, 0, 100), (90, 140, 255))
        green = cv2.inRange(tello_image, (0, 110, 0), (90, 255, 170))
        red = cv2.inRange(tello_image, (110, 0, 0), (255, 60, 120))


        true_display = resize(true_image, width=200)
        blue_display = resize(blue, width=200)
        green_display = resize(green, width=200)
        red_display = resize(red, width=200)


        cv2.imshow("red", red_display)
        cv2.imshow("green", green_display)
        cv2.imshow("blue", blue_display)
        
        cv2.imshow(window, true_display)
        cv2.waitKey(1)

        thresh = 100
        samples = 1000


        redSamples = 0
        greenSamples = 0
        blueSamples = 0
        for sample in range(samples):
            x = randint(0, 599)
            y = randint(0, 336)

            redSamples += red[y][x]
            greenSamples += green[y][x]
            blueSamples += blue[y][x]

        maxSamples = max(redSamples, greenSamples, blueSamples)
        if maxSamples >= thresh:
            if maxSamples == redSamples:
                color = "red"
            elif maxSamples == greenSamples:
                color = "green"
            else:
                color = "blue"

            hover(tello, 10)
            print()
            print("Color detected: " + color)
            tello.streamoff()
            tello.land()
            break
        else:
            color = "none"
            tello.send_keepalive()
        
        print(color, end="   \r")

            

    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("terminating...")
        break

tello.streamoff()
tello.land()