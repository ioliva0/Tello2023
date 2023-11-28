from json import load

def load_calibration():
    #Load camera calibration from json
    with open("Calibration/Calibration.json", "r") as calibration_file:
        calibration = load(calibration_file)
        calibration_file.close()
    #concave/convex distortion over the image
    return (calibration["Camera Matrix"], calibration["Distortion Coefficients"])