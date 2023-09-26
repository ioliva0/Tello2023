from threading import Thread
from time import time, sleep

def wait(length):
    start = time()
    end = start
    print("Initiating hover...")
    while (end - start < length):
        end = time()
        display_time = str(int(((end - start) * 1000) + 0.5) / 1000)
        print("Time elapsed: " + display_time, end="\r")
        sleep(0.01)
    print()
    print("Ending hover...")


def hover(tello, time, sim=False):
    timer = Thread(target=wait(time))

    if sim:
        sleep(time)
        return
    
    while timer.is_alive():
        tello.send_keepalive()

if __name__ == "__main__":
    hover(None, 10, True)