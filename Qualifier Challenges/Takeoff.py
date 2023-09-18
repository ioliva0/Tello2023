from time import sleep 
from Utils.TelloLib import *

init()

command("command")

command("takeoff")

sleep(15)
command("land")

sleep(5)
command("end")
