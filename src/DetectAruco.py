from djitellopy import tello, Tello
import cv2
from time import sleep

tello = Tello()

tello.connect()

tello.streamon()

#tello.takeoff()

window = "stream"

print("getting aruco stuff")
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

starting_image = cv2.imread("/Users/ioliva/Tello/Tello2023/selfie.png")
cv2.imshow(window, starting_image)

print("aruco stuff done")


while True:
    try:
        tello_image = tello.get_frame_read().frame
        rescaled = cv2.resize(tello_image, (640, 640))
        true_image = cv2.cvtColor(rescaled, cv2.COLOR_BGR2RGB)
        
        cv2.imshow(window, true_image)
        cv2.waitKey(1)
        tello.send_keepalive()

        try:
            print("trying to detect markers")
            (corners, ids, rejected) = arucoDetector.detectMarkers(true_image)
            print(ids)
            tags = cv2.aruco.drawDetectedMarkers(true_image, ids)
            cv2.imshow("tags", tags)
        except:
            pass
    except KeyboardInterrupt:
        tello.streamoff()
        #tello.land()
        print("terminating...")
        break
