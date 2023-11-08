from djitellopy import tello, Tello
import cv2

tello = Tello()

tello.connect()
tello.streamon()

window = "stream"
cv2.namedWindow(window)

image_num = 0

while True:
    try:
        tello.send_keepalive()

        tello_image = tello.get_frame_read().frame
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2GRAY)

        cv2.imshow(window, true_image)
        if cv2.waitKey(10) == ord("x"):
            cv2.imwrite("Calibration/Images/Calibration" + str(image_num) + ".png", true_image)
            print("Image " + str(image_num) + " written successfully")
            image_num += 1
    except KeyboardInterrupt:
        print("terminating...")
        break

tello.streamoff()