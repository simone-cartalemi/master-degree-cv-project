from enum import Enum

import numpy as np


class Model(Enum):
    V5_GRAM = "v5m_gram"
    V5_MIO = "v5m_mio"
    V8_MIO = "v8s_mio"

    def __str__(self):
        return self.value

V5_GRAM_WEIGHTS_PATH = "detection/weights/yolo v5/gram/exp/weights/best.pt"
V5_MIO_WEIGHTS_PATH = "detection/weights/yolo v5/mio/exp/weights/best.pt"
V8_MIO_WEIGHTS_PATH = "detection/weights/yolo v8/train/weights/best.pt"


BENCHMARK_PATH = "datasets/thai/"
BENCHMARK_LABELS_FILE = "all_vehicles_120_fps.csv"
VIDEO_RESOLUTION = (1920, 1080)
VIDEO_FRAME_PER_SECOND = 120
VIDEO_FORMAT = ".MOV"
MASK_PATH = "datasets/thai/masks/ROI_last.png"   # ROI_all.png

HOMOGRAPHY_MATRIX = np.load("homography/matrixes/thai_hom_matrix_last.npy")
CM_PER_PIXEL_RATIO = 300 / 69
VALIDATION_WINDOW = (800, 1070)
SPEED_WINDOW = (300, 800)

RESULTS_PATH = "results/"

EMISSION_COEFFICIENTS = {   # For 2025
    "diesel": (0.00580262, 0.00063457, 6.4831E-06, -1.446E-07, 2.3284E-09, -1.71E-11, 5.0932E-14),
    "petrol": (0.01185506, 0.00034041, 1.2578E-06, 1.0459E-07, -7.213E-10, 6.0958E-12, 0)
}

RATIO_FOR_DIESEL_FLEET = .55
RATIO_FOR_PETROL_FLEET = .45

TRACK_COLORS = [
    (255, 0, 0),    # Rosso
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Blu
    (255, 255, 0),  # Giallo
    (0, 255, 255),  # Ciano
    (255, 0, 255),  # Magenta
    (128, 0, 0),    # Marrone
    (0, 128, 0),    # Verde scuro
    (0, 0, 128),    # Blu scuro
    (128, 128, 0)   # Verde oliva
]
