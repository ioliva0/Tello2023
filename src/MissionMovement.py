from djitellopy import tello, Tello

from time import sleep

from Utils.Hover import hover

tello = Tello()

tello.connect()

try:
    tello.takeoff()
    
    tello.send_keepalive()
    sleep(5)
    tello.send_keepalive()

    tello.go_xyz_speed(50)

    tello.move_forward(381)
    tello.rotate_counter_clockwise(90) 
    tello.move_left(381)
    tello.move_left(381)
    tello.rotate_counter_clockwise(180)
    tello.move_left(381)
    tello.move_left(381)

    tello.land()
except:
    tello.land()