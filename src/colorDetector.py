from djitellopy import tello, Tello
import cv2
from imutils import grab_contours

tello = Tello()

tello.connect()

tello.streamon()

window = "stream"

starting_image = cv2.imread("/Users/ioliva/Tello/Tello2023/picture.png")
cv2.imshow(window, starting_image)

min_hsv = (70, 120, 50)
max_hsv = (100, 255, 255)

while True:
    try:
        tello_image = tello.get_frame_read().frame
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        mask = cv2.inRange(cv2.cvtColor(tello_image, cv2.COLOR_BGR2HSV), min_hsv, max_hsv)
        mask = cv2.dilate(mask, None, iterations=5)
        mask = cv2.erode(mask, None, iterations=5)

        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = grab_contours(contours)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(true_image, (x, y), (x+w, y+h), (0,0,0))
        
        cv2.imshow(window, true_image)
        cv2.imshow("mask", mask)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        tello.streamoff()
        print("terminating...")
        break