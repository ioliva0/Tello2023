from djitellopy import tello, Tello
import cv2
from imutils import resize
from random import randint
from Utils.Hover import hover
"""
tello = Tello()

tello.connect()

tello.streamon()

tello.takeoff()
"""
cap = cv2.VideoCapture(0)

window = "stream"

min_hsv = (70, 120, 50)
max_hsv = (100, 255, 255)

while True:
    try:

        #tello_image = tello.get_frame_read().frame
        #tello_image = resize(tello_image, width=600)

        #true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        ret, true_image = cap.read()
        tello_image = cv2.cvtColor(true_image, cv2.COLOR_RGB2BGR)

        pink = cv2.inRange(tello_image, (140, 100, 100), (180, 255, 255))
        purple = cv2.inRange(tello_image, (130, 0, 100), (180, 60, 255))
        blue = cv2.inRange(tello_image, (0, 0, 100), (90, 140, 255))
        light_blue = cv2.inRange(tello_image, (90, 0, 0), (130, 70, 120))
        green = cv2.inRange(tello_image, (0, 110, 0), (90, 255, 170))
        light_green = cv2.inRange(tello_image, (40, 50, 40), (90, 255, 255))    
        yellow = cv2.inRange(tello_image, (0, 100, 100), (90, 255, 255))
        orange = cv2.inRange(tello_image, (0, 50, 100), (90, 255, 255))
        red = cv2.inRange(tello_image, (110, 0, 0), (255, 60, 120))


        true_display = resize(true_image, width=200)
        pink_display = resize(orange, width=200)
        purple_display = resize(orange, width=200)
        blue_display = resize(blue, width=200)
        light_blue_display = resize(orange, width=200)
        green_display = resize(green, width=200)
        light_green_display = resize(orange, width=200)
        yellow_display = resize(orange, width=200)
        orange_display = resize(orange, width=200)
        red_display = resize(red, width=200)

        """
        cv2.imshow("red", red_display)
        cv2.imshow("orange", orange_display)
        cv2.imshow("yellow", yellow_display)
        cv2.imshow("light green", light_green_display)
        cv2.imshow("green", green_display)
        cv2.imshow("light blue", light_blue_display)
        cv2.imshow("blue", blue_display)
        cv2.imshow("purple", purple_display)
        cv2.imshow("pink", pink_display)
        """
        
        cv2.imshow(window, true_display)
        cv2.waitKey(1)

        thresh = 100
        samples = 1000

        redSamples = 0
        orangeSamples = 0
        yellowSamples = 0
        light_greenSamples = 0
        greenSamples = 0
        light_blueSamples = 0
        blueSamples = 0
        purpleSamples = 0
        pinkSamples = 0

        for sample in range(samples):
            x = randint(0, 599)
            y = randint(0, 336)

            redSamples += red[y][x]
            orangeSamples += orange[y][x]
            yellowSamples += yellow[y][x]
            light_greenSamples += light_green[y][x]
            greenSamples += green[y][x]
            light_blueSamples += light_blue[y][x]
            blueSamples += blue[y][x]
            purpleSamples += purple[y][x]
            pinkSamples += pink[y][x]

        maxSamples = max(redSamples, orangeSamples, yellowSamples, light_greenSamples, greenSamples, light_blueSamples, blueSamples, purpleSamples, pinkSamples)
        if maxSamples >= thresh:
            if maxSamples == redSamples:
                color = "red"
            elif maxSamples == orangeSamples:
                color = "orange"
            elif maxSamples == yellowSamples:
                color = "yellow"
            elif maxSamples == light_greenSamples:
                color = "light green"
            elif maxSamples == greenSamples:
                color = "green"
            elif maxSamples == light_blueSamples:
                color = "light blue"
            elif maxSamples == blueSamples:
                color = "blue"
            elif maxSamples == purpleSamples:
                color = "purple"
            else:
                color = "pink"

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