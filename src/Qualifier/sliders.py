import cv2
import numpy as np
from djitellopy import tello, Tello

tello = Tello()

tello.connect()

tello.streamon()

#cap = cv2.VideoCapture(1)
cv2.namedWindow('image')

def callback(x):
    pass

ilowH = 0
ihighH = 255

ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255

# create trackbars for color change
cv2.createTrackbar('lowR','image',ilowH,255,callback)
cv2.createTrackbar('highR','image',ihighH,255,callback)

cv2.createTrackbar('lowG','image',ilowS,255,callback)
cv2.createTrackbar('highG','image',ihighS,255,callback)

cv2.createTrackbar('lowB','image',ilowV,255,callback)
cv2.createTrackbar('highB','image',ihighV,255,callback)

while True:
    # grab the frame
    #ret, frame = cap.read()
    frame = tello.get_frame_read().frame

    # get trackbar positions
    ilowH = cv2.getTrackbarPos('lowR', 'image')
    ihighH = cv2.getTrackbarPos('highR', 'image')
    ilowS = cv2.getTrackbarPos('lowG', 'image')
    ihighS = cv2.getTrackbarPos('highG', 'image')
    ilowV = cv2.getTrackbarPos('lowB', 'image')
    ihighV = cv2.getTrackbarPos('highB', 'image')

    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #hsv = cv2.cvtColor(hsv, cv2.COLOR_RGB2BGR)


    lower_hsv = np.array([ilowH, ilowS, ilowV])
    higher_hsv = np.array([ihighH, ihighS, ihighV])
    mask = cv2.inRange(frame, lower_hsv, higher_hsv)

    frame = cv2.bitwise_and(frame, frame, mask=mask)

    # show thresholded image
    cv2.imshow('image', frame)
    k = cv2.waitKey(10) & 0xFF # large wait time to remove freezing
    if k == 113 or k == 27:
        break

cv2.destroyAllWindows()
