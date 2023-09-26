from djitellopy import tello, Tello

from Utils.Hover import hover

tello = Tello()

tello.connect()

print(str(tello.get_battery()) + "% Battery")

print("taking off")
tello.takeoff()

hover(tello, 15)

tello.land()