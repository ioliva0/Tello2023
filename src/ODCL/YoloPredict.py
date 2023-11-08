from ultralytics import YOLO

from os import listdir

# Load a model
model = YOLO('/home/cyber/Desktop/runs/detect/train/weights/best.pt')

dir = "/home/cyber/Downloads/unlabelledTennisBalls/data/test/tennis_ball/"

files = listdir(dir)
for file in files:
    result = model(dir + file, show=False, save=True)
    