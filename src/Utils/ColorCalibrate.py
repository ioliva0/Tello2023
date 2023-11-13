print("Please wait, initializing...", end="\r")
import cv2
from djitellopy import tello, Tello

tello = Tello()
tello.connect()
tello.streamon()

i = 0
while(i < 1000):
    print(cv2.waitKey(10))
    i += 1

print("Please put balloons of all 9 colors in front of the drone")
print("click on the Tello's video stream and press any key once all 9 ")



cv2.namedWindow()
cv2.waitKey(0)