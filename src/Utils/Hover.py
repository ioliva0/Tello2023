from threading import Thread
from time import time, sleep
from wait import wait

def hover(tello, time):
    timer = Thread(target=wait, args=[time, "hover"])
    
    timer.start()

    while timer.is_alive():
        #print("waiting...",end="\r")
        tello.send_keepalive()

if __name__ == "__main__":
    hover(None, 10)