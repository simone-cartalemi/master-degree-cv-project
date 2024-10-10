# Check Yolo v5 version
import cv2

import torch

import pathlib
import os

if os.name == 'nt':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath


def load_yolo_model(weights_path):
    try:
        model = torch.hub.load('detection/yolov5', 'custom', path=weights_path, source='local', verbose=False)
    except:
        os.makedirs("./detection/weights/yolo v5/", exist_ok=True)
        model = torch.hub.load('ultralytics/yolov5', model='yolov5n', verbose=False)
    model.eval()
    return model


weights_yolo5 = './detection/weights/yolo v5/best.pt'

model = load_yolo_model(weights_yolo5)

example_image = cv2.imread('./detection/src/test/example.png')

results = model(example_image)

results.print()
