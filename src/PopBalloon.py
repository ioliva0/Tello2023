from djitellopy import tello, Tello

from time import sleep

from Utils.Hover import hover

tello = Tello()

tello.connect()

print(str(tello.get_battery()) + "% Battery")

try:
    print("taking off")
    tello.takeoff()
    
    tello.send_keepalive()
    sleep(5)
    tello.send_keepalive()

    tello.go_xyz_speed(100, 0, 0, 100)
    tello.go_xyz_speed(-100, 0, 0, 100)

    tello.land()
except:
    tello.land()