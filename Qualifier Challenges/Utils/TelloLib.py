import threading 
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)

def command(command):
    print("command sent: " + command)
    sock.sendto(command.encode(encoding="utf-8"), tello_address)
    


def init():
    host = ''
    port = 9000
    locaddr = (host,port) 


    # Create a UDP socket

    sock.bind(locaddr)

    def recv():
        count = 0
        while True: 
            try:
                data, server = sock.recvfrom(1518)
                print(data.decode(encoding="utf-8"))
            except Exception:
                print ('\nExit . . .\n')
                break

    print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n       end')


    #recvThread create
    recvThread = threading.Thread(target=recv)
    recvThread.start()

    command("command")

def takeoff():
    command("takeoff")
def land():
    command("land")
def flip():
    command("flip")
def forward():
    command("forward")
def back():
    command("back")
def left():
    command("left")
def right():
    command("right")
def up():
    command("up")
def down():
    command("down")
def cw():
    command("cw")
def ccw():
    command("ccw")
def set_speed(speed):
    command("speed " + str(speed))
def get_speed():
    command("speed?")
def end():
    command("end")
    print ('connection terminating')
    sock.close()

"""
while True: 
    try:
        msg = input("")
        
        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        # Send data
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
    except:
        print("connection terminated")
        print ('\n . . .\n')
        sock.close()  
        break
"""