# Check Yolo v8 version
import cv2

import os

import ultralytics
ultralytics.checks()

from ultralytics import YOLO

def load_yolo_model(weights_path):
    try:
        model = YOLO(weights_path)
    except:
        os.makedirs("./detection/weights/yolo v8/", exist_ok=True)
        model = YOLO()
    return model


weights_yolo8 = './detection/weights/yolo v8/train/weights/best.pt'

model = load_yolo_model(weights_yolo8)

example_image = cv2.imread('./detection/src/test/example.png')

results = model(example_image)

print(results)
