from time import sleep 

from Utils.Version2 import Tello

drone = Tello.Tello()

print(drone.takeoff())
sleep(15)
print(drone.land())