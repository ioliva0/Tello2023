from djitellopy import tello, Tello

tello = Tello()

tello.connect()

print(str(tello.get_battery()) + "% Battery")

print("taking off")
tello.takeoff()

tello.curve_xyz_speed(50, 50, 0, 100, 0, 0, 50)
tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)

tello.land()