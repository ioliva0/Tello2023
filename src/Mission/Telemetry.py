if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import cv2
import Consts

def show_stream():
    true_image = cv2.cvtColor(Consts.tello_image, cv2.COLOR_BGR2RGB)

    #downscale and display the RGB image
    true_image_display = cv2.resize(true_image, [200, 150])
    cv2.imshow(Consts.main_window, true_image_display)
    print(true_image_display[0][0])

    cv2.waitKey(1)

def show_masks():
    for color in Consts.colors:
        #downscale and show each mask in its respective color window
        mask_display = cv2.resize(Consts.masks[color], [200, 150])
        cv2.imshow(color, mask_display)

    cv2.waitKey(1)

def show_all_images():
    show_stream()
    show_masks()

    #cv2.waitKey(0)

from json import dump

def output_results():

    with open("./src/Mission/Output/Mission.json", "w") as mission:
        dump(Consts.balloons, mission, indent=4)
        mission.close()
    
    with open("./src/Mission/Output/Raw.json", "w") as raw:
        dump(Consts.balloon_data, raw, indent=4)
        raw.close()