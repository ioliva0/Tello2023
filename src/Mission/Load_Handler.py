if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

from json import load
from numpy import array

def load_calibration():

    #return array([[929.77415147,0.,485.30477059],[0.,928.8631929,356.47846128],[0.,0.,1.]]), array([[0.00626081,-0.32400029,0.00146781,0.00277383,1.27535785]])

    #Load camera calibration from json
    with open("Calibration/Calibration.json", "r") as calibration_file:
        calibration = load(calibration_file)
        calibration_file.close()

    return array(calibration["Camera Matrix"]), array(calibration["Distortion Coefficients"])