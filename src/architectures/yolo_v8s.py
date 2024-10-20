from architectures.yolo import YOLO
import numpy as np

from ultralytics import YOLO as ym


class YOLO8(YOLO):

    def __init__(self, weights_path: str, _classes: dict):
        model = ym(weights_path)
        super().__init__(model, _classes)

    def detect_objects_in_frame(self, frame):
        results = self.model(frame, verbose=False)

        class_ids = []
        confidences = []
        boxes = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf.cpu().numpy().item()
                cls = box.cls.cpu().numpy().item()

                if conf > 0.5 and cls in list(self.classes.values()):
                    boxes.append([x1, y1, x2, y2])
                    confidences.append(conf)
                    class_ids.append(cls)

        return np.array(boxes), class_ids, confidences
