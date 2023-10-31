from djitellopy import tello, Tello
import cv2
from imutils import resize
from random import randint

tello = Tello()

tello.connect()
tello.streamon()
tello.takeoff()

margin = 100
thresh = 100
samples = 1000
imWidth = 600

def getImage():
    tello_image = tello.get_frame_read().frame
    tello_image = resize(tello_image, width=imWidth)

    #true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

    return tello_image

window = "stream"



def detectColor(image, minX=0, maxX=imWidth-1, minY=0, maxY=int(imWidth * 9 / 16)):

    blue = cv2.inRange(image, (0, 0, 100), (90, 140, 255))
    green = cv2.inRange(image, (0, 110, 0), (90, 255, 170))
    red = cv2.inRange(image, (110, 0, 0), (255, 60, 120))

    ###
    
    cv2.imshow("image", image)
    cv2.imshow("red", red)
    cv2.imshow("green", green)
    cv2.imshow("blue", blue)

    cv2.waitKey(1)
    #cv2.destroyAllWindows()
    
    ###

    redSamples = 0
    greenSamples = 0
    blueSamples = 0

    for sample in range(samples):
        x = randint(minX, maxX)
        y = randint(minY, maxY)

        redSamples += red[y][x] / 255
        greenSamples += green[y][x] / 255
        blueSamples += blue[y][x] / 255

    print("####################")
    print("red: " + str(redSamples))
    print("green: " + str(greenSamples))
    print("blue: " + str(blueSamples))
    print("####################")

    colors = {}

    if redSamples >= thresh:
        colors["red"] = redSamples
    if greenSamples >= thresh:
        colors["green"] = greenSamples
    if blueSamples >= thresh:
        colors["blue"] = blueSamples

    return colors

margin = 100

def balloonNotFound():
    tello.move_right(20)
    print("balloon not found, searching...")

target = "red"

print("##############################")
print("Target: " + target + " balloon")
print("##############################")

while True:
    try:
        tello.send_keepalive()

        tello_image = getImage()

        cv2.imshow(window, tello_image)
        cv2.waitKey(1)
        
        if target not in detectColor(tello_image):
            print("not in frame")
            balloonNotFound()
            continue

        center = int(imWidth / 2)

        colorsBySection = [
            detectColor(tello_image, 0, center - margin),
            detectColor(tello_image, center - margin, center + margin),
            detectColor(tello_image, center + margin, imWidth - 1)
        ]

        balloonSection = -1
        maxSamples = 0

        for currSection, colors in enumerate(colorsBySection):
            if target not in colors:
                continue

            currSamples = colors[target]
            if currSamples > maxSamples:
                balloonSection = currSection
                maxSamples = currSamples

        #Note: it is intentional that the drone moves to the left and to the right different amounts
        #this way it will eventually center on a balloon that's just off center
        match balloonSection:
            case -1:
                print("how the hell")
                balloonNotFound()
            case 0:
                print("balloon found to the left of drone")
                tello.move_left(20)
            case 2:
                print("balloon found to the right of drone")
                tello.move_right(25)
            case 1:
                cv2.imwrite("balloonPic.png", cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB))

                print("saved balloon image as balloonPic.png")
                print("moving to pop balloon")
                
                color = colorsBySection[1]
                """
                while target in color:
                    image = getImage()
                    color = detectColor(image, center - margin, center + margin)
                    tello.move_forward(30)
                """
                break

    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("terminating...")
        break

tello.land()
tello.streamoff()