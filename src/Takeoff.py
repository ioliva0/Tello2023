from time import sleep 

from .Utils.Version1 import Tello as Tello

drone = Tello.Tello()

print(drone.takeoff())
sleep(15)
print(drone.land())