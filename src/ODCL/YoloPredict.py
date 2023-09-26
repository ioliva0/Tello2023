from ultralytics import YOLO

from os import listdir

# Load a model
model = YOLO('/Users/ioliva/Tello/Tello2023/src/ODCL/runs/detect/train/weights/best.pt')

dir = "/Users/ioliva/Downloads/images.cv_47zzl2khrd26sjvnbipn7i/data/test/tennis_ball/"

files = listdir(dir)
for file in files:
    result = model(dir + file, show=False, save=True)