print("importing")
from djitellopy import tello, Tello
import cv2 
import os
import numpy as np
import imutils
from tensorflow import keras
print("imports complete")

"""
tello = Tello()

tello.connect()

tello.streamon()
"""

model = keras.models.load_model("IanIsTheBest.h5")
model.summary()

window = "stream"
#starting_image = cv2.imread("/Users/jwang/Tello/Tello2023/picture.png")
#cv2.imshow(window, starting_image)


#tello_image = tello.get_frame_read().frame

#imageList = ["img_five.JPG", "img_four.JPG", "img_one.JPG", "img_three.JPG", "img_two.JPG"]

true_image = cv2.imread("HandWrittenDigits/5.png")
true_image = cv2.cvtColor(true_image, cv2.COLOR_BGR2GRAY)

"""
## max contrast 
# read the input image
# changed from 'frame2' to frame
vid = cv2.imread('frame')
"""

# define the alpha and beta
contrast = 100 #17 # Contrast control (0~127)
brightness = 1 #1 # Brightness control (0~100)

# call convertScaleAbs function
scaleAbs = cv2.convertScaleAbs(true_image, contrast, brightness)

# display the output image

## 28x28
#number_arr = np.asarray(tello_image) 

#img_resized = imutils.resize(scaleAbs, height = 28, width = 28)
img_resized = cv2.resize(scaleAbs, (28,28))  

# change brightness
for row in range(len(img_resized)):
    for column in range(len(img_resized[row])):
        if img_resized[row][column] > 130: 
            img_resized[row][column] = 0
        else: 
            img_resized[row][column] = 255

# crop image to 28x28
center = int(len(img_resized[0])/2)
img_resized = img_resized[0 : 28, center-14 : center+14] 


# cannot detech image, issue with input sizes
print(img_resized.shape)

# set breakpoint - debugger
'''flatImg = img_resized.reshape((1, 784))

print(flatImg)
print(flatImg.shape)'''

img_resized = img_resized.reshape((1, 28, 28, 1))

prediction = model.predict(img_resized)
predicted_digit = np.argmax(prediction) 

print(f"Predicted Digit: {predicted_digit}")

# hand draw 5 number
# save them into project file
# replace code to interface w/ webcame 
