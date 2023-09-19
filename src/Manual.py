import Utils.Version1.Tello as Tello
import Utils.Version1.TelloUI as TelloUI

drone = Tello.Tello()  
vplayer = TelloUI(drone)
vplayer.root.mainloop()