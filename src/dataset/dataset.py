from abc import ABC, abstractmethod


class Dataset(ABC):
    VEHICLE_CLASSES = {}

    @abstractmethod
    def get_labels(self, labels_path):
        raise NotImplementedError("Il metodo load_labels deve essere implementato nelle sottoclassi")
