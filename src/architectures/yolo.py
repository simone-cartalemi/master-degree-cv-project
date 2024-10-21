from abc import ABC, abstractmethod


class YOLO(ABC):
    model = None
    classes = {}

    def __init__(self, _model, _classes: dict) -> None:
        super().__init__()
        self.model = _model
        self.classes = _classes

    @abstractmethod
    def detect_objects_in_frame(self, frame):
        raise NotImplementedError("Il metodo detect_objects_in_frame deve essere implementato nelle sottoclassi")
