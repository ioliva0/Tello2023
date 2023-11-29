if __name__ == "__main__":
    print("Error: This script is not a standalone; please run Main.py")
    exit()

import numpy
import cv2
from math import sin, cos
import Consts

#https://stackoverflow.com/questions/75750177/solve-pnp-or-estimate-pose-single-markers-which-is-better
def estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    marker_points = numpy.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=numpy.float32)
    
    success, rotation_vector, translation_vector = cv2.solvePnP(marker_points, corners, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)

    translation_vector = [int(pos[0] * 10) / 10 for pos in translation_vector]
    translation_vector = (translation_vector[0], translation_vector[2])

    rotation_vector = [int(angle[0] * 10) / 10 for angle in rotation_vector]
    rotation = rotation_vector[2]

    return translation_vector, rotation

def find_balloon_center(corners):
    translation_vector, rotation = estimatePoseSingleMarkers(corners, Consts.tag_size_in, Consts.calibration[0], Consts.calibration[1])

    x_offset = sin(rotation) * Consts.balloon_radius_in
    z_offset = cos(rotation) * Consts.balloon_radius_in

    x = int((translation_vector[0] + x_offset) * 10) / 10
    z = int((translation_vector[1] + z_offset) * 10) / 10

    return x, z