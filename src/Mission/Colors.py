if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

from Consts import colors

#helper method to create a dictionary of structure {color : number} for all colors
def create_color_dict():
    dict = {}
    for color in colors():
        dict[color] = 0
    return dict