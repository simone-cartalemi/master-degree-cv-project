import numpy as np

MODELS = ["v5m_gram", "v5m_mio", "v8s_mio"]


#BENCHMARK_PATH = "../datasets/thai/"
VIDEO_RESOLUTION = (1920, 1080)
VIDEO_FRAME_PER_SECOND = 120
VIDEO_FORMAT = ".mov"

HOMOGRAPHY_MATRIX = np.load("../homography/matrixes/thai_hom_matrix_last.npy")
CM_PER_PIXEL_RATIO = 300 / 69
VALIDATION_WINDOW = (800, 1070)
SPEED_WINDOW = (200, 800)

RESULTS_PATH = "../experiments/"

EMISSION_COEFFICIENTS = {
    "diesel": (0.00580262, 0.00063457, 6.4831E-06, -1.446E-07, 2.3284E-09, -1.71E-11, 5.0932E-14),
    "petrol": (0.01185506, 0.00034041, 1.2578E-06, 1.0459E-07, -7.213E-10, 6.0958E-12, 0)
}


