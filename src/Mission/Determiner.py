if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import Consts

def determine_color(key):
    max_color = ""
    max_confidence = 0
    for color in Consts.balloon_data[key]["Color_Confidences"]:
        if Consts.balloon_data[key]["Color_Confidences"][color] >= max_confidence:
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