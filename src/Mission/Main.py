#Imports

import time

import Config
import Consts
import Initializer
from Sweeper import sweep

Initializer.initialize_tello()

Initializer.initialize_cv2()

Initializer.takeoff()

exit()

tello = Consts.tello

y = 0
dir = None

def pop_target():

    if not Config.target:
        print("Drone target popping disabled, target not popped")
        return False

    if not Config.target or len(Consts.balloons) <= 0:
        print("No balloons detected, target not popped")
        return False
    
    for balloon in Consts.balloons:
        if balloon["ID"] == Consts.target_tag and balloon["Color"] == Consts.target_color:
            if Config.true_movement:
                tello.move_right(balloon["Position"][0])
                tello.move_forward(balloon["Position"][1])
                tello.move_back(50)
            print("Balloon (theoretically) popped")
            return True
    
    print("Balloon not found in balloon list")
    return False

try:
    if Config.true_movement:
        tello.move_forward(Consts.size)
        tello.rotate_counter_clockwise(90)
    else:
        print("True movement disabled, faking movement with sleep statements")

    Consts.current_y = Consts.size
    Consts.current_dir = -1

    #sweep to the left, downwards from top
    sweep_balloons = sweep()
    sweep_balloons = sweep()
    Consts.current_dir = 1

    #sweep to the right, upwards from bottom
    sweep_balloons = sweep()
    sweep_balloons = sweep()

    if Config.true_movement:
        tello.rotate_counter_clockwise(90)
        tello.move_back(Consts.current_y)
    Consts.current_y = 0

    print(Consts.balloons)

    pop_target()

except Exception as e:
    tello.streamoff()
    if Config.takeoff:
        tello.land()
    raise e

tello.streamoff()

if Config.takeoff:
    tello.land()