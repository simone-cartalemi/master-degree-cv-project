# Check Yolo v5 version
import cv2

import torch

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def load_yolo_model(weights_path):
    model = torch.hub.load('detection/yolov5', 'custom', path=weights_path, source='local', verbose=False)
    model.eval()
    return model


weights_yolo5 = './detection/weights/yolo v5/best.pt'

model = load_yolo_model(weights_yolo5)

example_image = cv2.imread('./detection/src/test/example.png')

results = model(example_image)

print(results)
