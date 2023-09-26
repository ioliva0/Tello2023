print("importing keras...")
from tensorflow import keras
print("imports complete")

model_name = "Mnist/model1"

model = keras.models.load_model("./src/ODCL/Trained/" + model_name + ".h5")
model.summary()