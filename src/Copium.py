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
tello.move_up(40)

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
    
    pink = cv2.inRange(image, (216, 131, 173), (255, 173, 209))
    purple = cv2.inRange(image, (55, 17, 74), (85, 66, 123))
    blue = cv2.inRange(image, (14, 74, 117), (59, 115, 171))
    light_blue = cv2.inRange(image, (76, 117, 180), (158, 187, 225))
    green = cv2.inRange(image, (117, 117, 0), (43, 169, 69))
    light_green = cv2.inRange(image, (88, 174, 74), (116, 255, 170))    
    yellow = cv2.inRange(image, (167, 122, 0), (201, 161, 49))
    orange = cv2.inRange(image, (138, 15, 0), (214, 65, 13))
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

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

target = input("Target ID: ")



t1 = Thread(target=missionMovement)

t1.start()

while t1.is_alive():
    detectColor()

tello.streamoff()
tello.land()