from time import sleep 
from Utils.Version1.TelloLib import *

init()

takeoff()

sleep(15)
land()

sleep(5)
end()
