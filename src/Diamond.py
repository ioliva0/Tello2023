from djitellopy import tello, Tello

from math import sqrt

sidelen = int(sqrt(2) * 100 / 2 + 0.5)

tello = Tello()

tello.connect()

print(str(tello.get_battery()) + "% Battery")

print("taking off")
tello.takeoff()

tello.go_xyz_speed(sidelen, sidelen, 0, 50)
tello.go_xyz_speed(-sidelen, sidelen, 0, 50)
tello.go_xyz_speed(-sidelen, -sidelen, 0, 50)
tello.go_xyz_speed(sidelen, -sidelen, 0, 50)

tello.land()