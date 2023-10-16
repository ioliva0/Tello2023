from djitellopy import tello, Tello

from Utils.Hover import hover

tello = Tello()

tello.connect()
tello.takeoff()
tello.streamon()

def draw_num(tagNum):
    print("############")
    print("Drawing number: " + tagNum)
    print("############")

    match tagNum: 
        case 0:
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(50, 50, 0, 100, 0, 0, 50)
        case 1:
            tello.go_xyz_speed(-100, 0, 0, 50)
        case 2:
            tello.curve_xyz_speed(-50, 50, 0, -100, 0, 0, 50)
        case 3:
            tello.curve_xyz_speed(-25, 50, 0, -50, 0, 0)
            tello.curve_xyz_speed(-25, 50, 0, -50, 0, 0)
        case 4:
            tello.go_xyz_speed(-50, -50, 0, 50)
            tello.go_xyz_speed(0, 50, 0, 50)
            tello.go_xyz_speed(-50, 0, 0, 50)
            tello.go_xyz_speed(100, 0, 0, 50)
        case 5:
            tello.go_xyz_speed(0, -50, 0, 50)
            tello.go_xyz_speed(-50, 0, 0, 50)
            tello.curve_xyz_speed(-25, 25, 0, -50, 0, 0, 50)
        case 6:
            tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 50)
            tello.curve_xyz_speed(25, 25, 0, 50, 0, 0, 50)
        case 7:
            tello.go_xyz_speed(0, 50, 0, 50)
            tello.go_xyz_speed(-100, -50, 0, 50)
        case 8:
            tello.curve_xyz_speed(-25, -25, 0, -50, 0, 0, 50)
            tello.curve_xyz_speed(-25, 25, 0, -50, 0, 0, 50)
            tello.curve_xyz_speed(25, -25, 0, 50, 0, 0, 50)
            tello.curve_xyz_speed(25, 25, 0, 50, 0, 0, 50)
        case 9:
            tello.curve_xyz_speed(-25, -25, 0, -50, 0, 0, 50)
            tello.curve_xyz_speed(25, 25, 0, 50, 0, 0, 50)
            tello.curve_xyz_speed(-50, 50, 0, -100, 0, 0, 50)

    #tello.land()
    hover(tello, 5)

for num in range(0, 10, 1):
    draw_num(num)