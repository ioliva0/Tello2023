from Consts import colors

#helper method to create a dictionary of structure {color : number} for all colors
def create_color_dict():
    dict = {}
    for color in colors():
        dict[color] = 0
    return dict