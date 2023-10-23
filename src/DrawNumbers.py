from djitellopy import tello, Tello
import cv2
from Utils.Hover import hover

tello = Tello()

tello.connect()
tello.takeoff()
#tello.streamon()

def draw_num(tagNum):
    print("############")
    print("Drawing number: " + str(tagNum))
    print("############")

    match tagNum: 
        case 0:
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(50, 50, 0, 100, 0, 0, 50)
        case 1:
            tello.go_xyz_speed(-100, 0, 0, 50)
        case 2:
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
            tello.go_xyz_speed(0, -100, 0, 50)
        case 3:
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
        case 4:
            tello.go_xyz_speed(-50, 50, 0, 50)
            tello.go_xyz_speed(0, -50, 0, 50)
            tello.go_xyz_speed(-50, 0, 0, 50)
            tello.go_xyz_speed(100, 0, 0, 50)
        case 5:
            tello.go_xyz_speed(0, 50, 0, 50)
            tello.go_xyz_speed(-50, 0, 0, 50)
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
        case 6:
            tello.curve_xyz_speed(-100, 100, 0, -200, 0, 0, 50)
            tello.curve_xyz_speed(50, -50, 0, 100, 0, 0, 50)
        case 7:
            tello.go_xyz_speed(0, -50, 0, 50)
            tello.go_xyz_speed(-100, 50, 0, 50)
        case 8:
            tello.curve_xyz_speed(-50, 50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(50, 50, 0, 100, 0, 0, 50)
            tello.curve_xyz_speed(50, -50, 0, 100, 0, 0, 50)
        case 9:
            tello.curve_xyz_speed(-50, 50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(50, -50, 0, 100, 0, 0, 50)
            tello.curve_xyz_speed(-100, -100, 0, -200, 0, 0, 50)
    #hover(tello, 6)

# Create a window for the video stream
window = "Tello Stream"
cv2.namedWindow(window)

# Define the ArUco dictionary
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

while True:
    try:

        tello.send_keepalive()
        tello_image = tello.get_frame_read().frame

        # Resize the image for display
        #true_image = cv2.resize(tello_image, (640, 480))
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)

        # Detect ArUco markers in the image
        corners, ids, rejected = arucoDetector.detectMarkers(true_image)

        # If ArUco markers are detected, print their IDs
        if ids is not None:
            draw_num(ids[0])
            #tello.land()
            break

    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("Terminating...")
        break

tello.land()