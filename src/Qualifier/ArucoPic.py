from djitellopy import tello, Tello
import cv2
import numpy as np

# Create a Tello instance
tello = Tello()

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
            for i in range(len(ids)):
                aruco_id = ids[i][0]
                print(f"ArUco Tag ID: {aruco_id}")

        # Draw detected markers on the image
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(true_image, corners, ids)
            cv2.imwrite("arucotag.jpg", true_image)
            tello.land()

        # Convert the image to BGR color format for display

        # Display the image in the window
        cv2.imshow(window, true_image)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("Terminating...")
        break