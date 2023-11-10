from time import time, sleep

def wait(length, action_name):
    start = time()
    end = start
    print("Initiating " + action_name + "...")
    while (end - start < length):
        end = time()
        display_time = str(int(((end - start) * 1000) + 0.5) / 1000)
        print("Time elapsed: " + display_time, end="\r")
        sleep(0.01)
    print()
    print("Ending " + action_name + "...")
