from djitellopy import tello, Tello

tello = Tello()

tello.connect()

print(str(tello.get_battery()) + "% Battery")

print("taking off")
tello.takeoff()

tello.move_right(100)
tello.move_forward(100)
tello.move_left(100)
tello.move_back(100)

tello.land()