import Utils.Version2.Tello as Tello

import Utils.Version2.TelloUI as TelloUI

def main():

    drone = Tello.Tello()  

    vplayer = TelloUI(drone)

    vplayer.root.mainloop() 

if __name__ == '__main__':
    main()