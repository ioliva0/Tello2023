if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import Consts

from statistics import median

def determine_color(key):
    max_color = ""
    max_confidence = 0

    median_hue_score = median(Consts.balloon_data[key]["Hue_Scores"])

    for color in Consts.balloon_data[key]["Color_Confidences"]:
        
        color_hue_score = abs(median_hue_score - Consts.hues[color])

        hue_confidence = min(200, 3000 / (color_hue_score ** 3)) / 2

        hue_penalty = 2 ** (1/5 * abs(color_hue_score))

        rgb_confidence = Consts.balloon_data[key]["Color_Confidences"][color]

        if rgb_confidence + hue_confidence - hue_penalty >= max_confidence:
            max_confidence = Consts.balloon_data[key]["Color_Confidences"][color]
            max_color = color
    return max_color

def determine_position(key):    
    positions = []

    for i in range(len(Consts.balloon_data[key]["Y_Values"])):
        
        sideways_distance = Consts.balloon_data[key]["Translation_Vectors"][i][0] / 12
        forwards_distance = Consts.balloon_data[key]["Translation_Vectors"][i][1] / 12
        drone_y = Consts.balloon_data[key]["Y_Values"][i] / (2.54 * 12)
        dir = Consts.current_dir

        positions.append((forwards_distance * dir, drone_y + sideways_distance * -dir))
    
    avg_position = [0,0]

    for position in positions:
        avg_position[0] += position[0] / len(positions)
        avg_position[1] += position[1] / len(positions)

    return avg_position
    
def determine_balloon(id):

    key = str(id)

    print("Determining balloon of tag " + key)

    balloon = {}
    balloon["ID"] = id

    balloon["Color"] = determine_color(key)
    
    balloon["Position"] = determine_position(key)

    Consts.balloons.append(balloon)

def determine_results():
    for id in Consts.balloon_data:
        determine_balloon(id)