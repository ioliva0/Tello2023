from ultralytics import YOLO

model = YOLO("/Users/ioliva/Tello/Tello2023/src/ODCL/runs/detect/train2/weights/last.pt")

# Train the model using the 'coco128.yaml' dataset for 3 epochs
results = model.train(data="/Users/ioliva/Downloads/tennisball.v1i.yolov8/data.yaml", epochs=50, resume=True)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model('https://www.wbs.ac.uk/sites/wbs2020/cache/file/57F11F62-A223-644C-F600F8EAB5706993.jpg', save=True, device='mps')

# Export the model to ONNX format
success = model.export(format='onnx')