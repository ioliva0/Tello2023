from djitellopy import tello, Tello
import cv2

tello = Tello()

tello.connect()

tello.streamon()

tello.takeoff()

window = "stream"

while True:
    try:
        tello_image = tello.get_frame_read().frame
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)
        cv2.imshow(window, true_image)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("terminating...")
        break