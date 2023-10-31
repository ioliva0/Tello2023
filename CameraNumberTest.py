print("importing")
import cv2 
import numpy as np
from tensorflow import keras
from imutils import resize
print("imports complete")

model = keras.models.load_model("IanIsTheBest.h5")
model.summary()

window = "stream"

def predict(num):
    path = "HandWrittenDigits/" + str(num) + ".png"
    print("Prediction for file at " + path)
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    resized = resize(image, height=28)
    #crop image to 28x28

    if len(resized[0]) < 28:
        resized = resize(image, width=28)

    center_col = int(len(resized[0])/2)
    center_row = int(len(resized)/2)

    image = resized[center_row-14 : center_row+14, center_col-14 : center_col+14] 

    # change brightness
    for row in range(len(image)):
        for column in range(len(image[row])):
            if image[row][column] > 130: 
                image[row][column] = 0
            else: 
                image[row][column] = 255

    image = image.reshape((1, 28, 28, 1))

    prediction = model.predict(image)
    #print("confidences: " + str(prediction))
    predicted_digit = np.argmax(prediction) 

    print(f"Predicted Digit: {predicted_digit}")

#chosen number images
nums = [0, 2, 3, 4, 6, 7, 9]

for num in nums:
    print("Actual Digit: " + str(num))
    predict(num)
    print("_________________________________________________________________")