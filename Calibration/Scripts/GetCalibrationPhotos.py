from djitellopy import tello, Tello
import cv2

tello = Tello()

tello.connect()
tello.streamon()

window = "stream"
cv2.namedWindow(window)

"""
tello_image = tello.get_frame_read()
cv2.waitKey(0)
tello_image = tello.get_frame_read().frame
cv2.imshow(window, tello_image)
cv2.waitKey(1000)
"""

image_num = 0

while True:
    try:
        tello.send_keepalive()

        tello_image = tello.get_frame_read().frame
        tello_image = cv2.resize(tello_image, [200, 150])
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2GRAY)

        cv2.imshow(window, true_image)
        
        if cv2.waitKey(100) == ord("x"):
            cv2.imwrite("Calibration/Images/Calibration" + str(image_num) + ".png", true_image)
            print("Image " + str(image_num) + " written successfully")
            image_num += 1
    except KeyboardInterrupt:
        print("terminating...")
        break

tello.streamoff()