from djitellopy import tello, Tello
import cv2
from time import sleep

tello = Tello()

tello.connect()

tello.streamon()

#tello.takeoff()

window = "stream"

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

starting_image = cv2.imread("/Users/ioliva/Tello/Tello2023/picture.png")
cv2.imshow(window, starting_image)


while True:
    try:
        tello_image = tello.get_frame_read().frame
        
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB).resize((640, 640))

        try:
            (corners, ids, rejected) = arucoDetector.detectMarkers(true_image)
            tags = cv2.aruco.drawDetectedMarkers(true_image, ids)
            cv2.imshow("tags", tags)
        except:
            pass

        
        cv2.imshow(window, true_image)
        cv2.waitKey(1)
        tello.send_keepalive()
        print("IDS DETECTED: " + str([1]))
    except KeyboardInterrupt:
        tello.streamoff()
        #tello.land()
        print("terminating...")
        break
