from architectures.yolo import YOLO
import numpy as np
import torch

import warnings
import pathlib
import os


class YOLO5(YOLO):

    def __init__(self, weights_path: str, _classes: dict):
        self.check_path_os()
        #model = torch.hub.load("ultralytics/yolov5", "yolov5m")
        model = torch.hub.load('detection/yolov5', 'custom', path=weights_path, source='local', verbose=False)
        model.eval()
        super().__init__(model, _classes)

    def check_path_os(self):
        if os.name == 'nt':
            temp = pathlib.PosixPath
            pathlib.PosixPath = pathlib.WindowsPath

    def silence_warning(self):
        warnings.filterwarnings("ignore", category=FutureWarning)

    def detect_objects_in_frame(self, frame):
        results = self.model(frame)

        detections = results.xyxy[0].cpu().numpy()

        class_ids = []
        boxes = []
        confidences = []

        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            if conf > 0.5 and cls in list(self.classes.values()):
                boxes.append([x1, y1, x2, y2])
                confidences.append(conf.item())
                class_ids.append(int(cls))

        return np.array(boxes), class_ids, confidences
