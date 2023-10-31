from djitellopy import tello, Tello
import cv2
from imutils import resize

# Create a Tello instance
tello = Tello()

def flip(num_flips):
    for i in range(num_flips):
        print("Flips: " + str(i + 1) + "/" + str(num_flips))
        if i % 2 == 0:
            tello.flip_back()
        else:
            tello.flip_forward()
        #sleep(1)

# Connect to the Tello and start the video stream
tello.connect()
tello.streamon()
tello.takeoff()

# Create a window for the video stream
window = "Tello Stream"
cv2.namedWindow(window)

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

target = 4
print("#####################")
print("TARGET: " + str(target))
print("#####################")

while True:
    try:
        
        tello.send_keepalive()
        tello_image = tello.get_frame_read().frame

        tello_image = resize(tello_image, width=600)
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)


        #how close the ArUCo tag needs to be to the center of the stream to register
        #from 0 to 300, 300 is anywhere on the screen, 0 is never
        #center_tolerance = 200
        
        #crops the image with an array slice (images are stored row major)
        #image_center = true_image[0 : -1][300 - center_tolerance: 300 + center_tolerance]
        corners, ids, rejected = arucoDetector.detectMarkers(true_image)  

        print("still searching for ArUCo tag")
        tello.move_right(30)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(true_image, corners, ids)
            if target in ids[0]:
                cv2.imwrite("flipTag.png", true_image)
                flip(target)
                break
            
        #cv2.imshow("window", image_center)
        cv2.imshow("window2", true_image)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        break

print("Terminating...")
tello.streamoff()
tello.land()