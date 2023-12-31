from djitellopy import tello, Tello
import cv2
from time import sleep

tello = Tello()

tello.connect()

tello.streamon()

tello.takeoff()

sleep(2)

tello.move_up(40)


window = "stream"

starting_image = cv2.imread("/Users/ioliva/Tello/Tello2023/picture.png")
cv2.imshow(window, starting_image)

while True:
    try:
        tello_image = tello.get_frame_read().frame
        true_image = cv2.cvtColor(tello_image, cv2.COLOR_BGR2RGB)
        cv2.imshow(window, true_image)
        if cv2.waitKey(10) == ord("x"):
            cv2.imwrite("selfie.png", true_image)
        tello.send_keepalive()
    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        print("terminating...")
        break