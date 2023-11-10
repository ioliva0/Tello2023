from djitellopy import tello, Tello
import cv2
from imutils import resize
from random import randint
from time import sleep
from Utils.Hover import hover
from threading import Thread

tello = Tello()

tello.connect()
tello.streamon()
tello.takeoff()

cap = cv2.VideoCapture(0)

margin = 100
thresh = 100
samples = 1000
imWidth = 600

window = "stream"

def getImage():
    image = tello.get_frame_read().frame
    image = resize(image, width=imWidth)

    true_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image, true_image

def detectColor(image, minX=0, maxX=imWidth-1, minY=0, maxY=int(imWidth * 9 / 16)):

    image, true_image = getImage()
    
    pink = cv2.inRange(image, (182, 121, 157), (212, 173, 211))
    purple = cv2.inRange(image, (102, 78, 150), (186, 122, 203))
    blue = cv2.inRange(image, (14, 74, 117), (59, 115, 171))
    light_blue = cv2.inRange(image, (67, 132, 129), (99, 153, 175))
    green = cv2.inRange(image, (17, 117, 0), (43, 169, 69))
    light_green = cv2.inRange(image, (88, 174, 74), (116, 255, 170))    
    yellow = cv2.inRange(image, (169, 87, 0), (236, 255, 15))
    orange = cv2.inRange(image, (182, 55, 0), (255, 147, 62))
    red = cv2.inRange(image, (161, 0, 43), (255, 72, 113))

    cv2.imshow("red", red_display)
    cv2.imshow("orange", orange_display)
    cv2.imshow("yellow", yellow_display)
    cv2.imshow("light green", light_green_display)
    cv2.imshow("green", green_display)
    cv2.imshow("light blue", light_blue_display)
    cv2.imshow("blue", blue_display)
    cv2.imshow("purple", purple_display)
    cv2.imshow("pink", pink_display)

    true_display = resize(true_image, width=200)
    pink_display = resize(pink, width=200)
    purple_display = resize(purple, width=200)
    blue_display = resize(blue, width=200)
    light_blue_display = resize(light_blue, width=200)
    green_display = resize(green, width=200)
    light_green_display = resize(light_green, width=200)
    yellow_display = resize(yellow, width=200)
    orange_display = resize(orange, width=200)
    red_display = resize(red, width=200)
    
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

        print()
    else:
        color = "none"
        tello.send_keepalive()
    
    print(color, end="   \r")

def missionMovement():
    tello.go_xyz_speed(50)

    tello.move_forward(381)
    tello.rotate_counter_clockwise(90) 
    tello.move_left(381)
    tello.move_left(381)
    tello.rotate_counter_clockwise(180)
    tello.move_left(381)
    tello.move_left(381)

t1 = Thread(target=missionMovement)

t1.start()

while t1.is_alive():
    detectColor()

tello.streamoff()
tello.land()