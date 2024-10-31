import cv2
import numpy as np

from config.defaults import HOMOGRAPHY_MATRIX, CM_PER_PIXEL_RATIO, SPEED_WINDOW, VIDEO_FRAME_PER_SECOND


def centroid(bbox: list) -> tuple:
    '''
    Calculate center point of bounding box
    '''
    x1, y1, x2, y2 = bbox
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    return (center_x, center_y)

def remap_point(point: tuple = ()) -> tuple:
    '''
    Apply homography matrix to point
    '''
    p_h = np.array([[point]], dtype='float32')
    transformed_point_array = cv2.perspectiveTransform(p_h, HOMOGRAPHY_MATRIX)
    return tuple(transformed_point_array[0][0])

def frame_to_kmph(initial_point: tuple, final_point: tuple, frames_difference: int, frame_rate: int = VIDEO_FRAME_PER_SECOND, cm_per_pixel: float = CM_PER_PIXEL_RATIO) -> float:
    '''
    Get speed from points p_i and p_f and time of apparition.

    Calculate distance between frames in pixel (euclidean distance between p_i and p_f),
    Convert distanze from pixel to meters,
    Get time in seconds,
    Calculate kmph
    Return float rounded at 2 digit
    '''
    distance = np.sqrt((final_point[0] - initial_point[0]) ** 2 + (final_point[1] - initial_point[1]) ** 2)
    distance_meters = (distance * cm_per_pixel) / 100
    secs = frames_difference / frame_rate
    speed = (3.6 * distance_meters) / secs
    return round(speed, 2)

def linear_speed(positions: dict, instant_treshold: int = 60) -> float|None:
    '''
    Calculate the vehicle speed between initial and final position (linear mean)
    Appearances shorter than instant_treshold will be discarded

    Calculate only a range of points 200 <= y <= 800 filtered from all (more precision away from frame borders) for more precision
    This range match in homography space at around 24 meters.
    '''
    filtered_positions = {k: v for k, v in positions.items() if v[1] >= SPEED_WINDOW[0] and v[1] <= SPEED_WINDOW[1]}
    if not len(filtered_positions):
        return None
    
    sorted_keys = sorted(filtered_positions.keys())
    f_index = sorted_keys[-1]
    i_index = sorted_keys[0]
    frames_difference = f_index - i_index + 1

    # Remove instantanely apparition (less than 60 frames)
    if frames_difference < instant_treshold:
        return None
    
    initial_point = remap_point(filtered_positions[i_index])
    final_point = remap_point(filtered_positions[f_index])
    return frame_to_kmph(initial_point, final_point, frames_difference)
