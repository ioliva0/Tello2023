from djitellopy import tello, Tello
import cv2
from imutils import resize

# Create a Tello instance
tello = Tello()

tello.connect()
tello.streamon()
print(str(tello.get_battery()) + "% Battery")
tello.takeoff()

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

target = 3

def move_to_tag():
    tello.send_keepalive()
    tello_image = tello.get_frame_read().frame

    tello_image = resize(tello_image, width=600)
    true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

    tolerance = 100

    corners, ids, rejected = arucoDetector.detectMarkers(true_image)

    #cv2.rectangle(true_image, (200, -100), (400, 500), (255,255,255), thickness=10)
    cv2.imshow("window", true_image)
    cv2.waitKey(1)

    if ids is None:
        print("no tags found")
        #tello.move_left(20)
        return 1

    for i, id in enumerate(ids):
        if id != target:
            continue
        
        avg_x = 0
        for corner in corners[i][0]:
            avg_x += corner[0]
        avg_x /= 4.0
        
        if avg_x < 300 - tolerance:
            print("left, " + str(avg_x), end="  \r")
            tello.move_left(20)
        elif avg_x > 300 + tolerance:
            print("right, " + str(avg_x), end="  \r")
            tello.move_right(20)
        else:
            print("center, " + str(avg_x), end="  \r")
            tello.move_forward(40)
            return 0

    print("target not in view")
    #tello.move_left(20)
    return 1

while True:
    try:
        if move_to_tag() == 0: 
            break

        key = cv2.waitKey(100)
        if key == ord("1"):
            print("switching to target 1")
            target = 1
        elif key == ord("2"):
            print("switching to target 2")
            target = 2
        elif key == ord("3"):
            print("switching to target 3")
            target = 3
    except KeyboardInterrupt:
        break

print("Terminating...")
tello.streamoff()
#tello.land()