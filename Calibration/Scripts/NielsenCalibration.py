#created by Nicolai Nielsen https://github.com/niconielsen32/ComputerVision/blob/37b279fa44e28fe3ea859bc8f14f5353a6b93e54/cameraCalibration.py

import numpy as np
import cv2 as cv
import glob
import json

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

#"""
chessboardSize = (7, 7)
#frameSize = (1830,1330)
frameSize = (960, 720)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('Calibration/Images/*')

for image in images:

    img = cv.imread(image)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        print("hi")

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        
        
        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(1000)

cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

print(cameraMatrix)
print(dist)

cameraMatrix = cameraMatrix.tolist()
dist = dist.tolist()

rvecs = [rvec.tolist() for rvec in rvecs]
tvecs = [tvec.tolist() for tvec in tvecs]

calibration = {
    "Camera Matrix" : cameraMatrix,
    "Distortion Coefficients" : dist,
    "Rotation Vectors" : rvecs,
    "Transformation Vectors" : tvecs
}

with open("Calibration/Calibration.json", 'w') as calibrationFile:
    jsonString = json.dump(calibration, calibrationFile, indent=2)
    #calibrationFile.write(str(calibration))
    calibrationFile.close()