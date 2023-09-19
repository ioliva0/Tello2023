from time import sleep 

import Utils.Version1.Tello as Tello

drone = Tello.Tello()

print(drone.takeoff())
sleep(15)
print(drone.land())