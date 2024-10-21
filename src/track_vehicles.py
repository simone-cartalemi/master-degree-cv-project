from architectures.yolo_v5m import YOLO5
from architectures.yolo_v8s import YOLO8

import datetime
import sys
import os

import cv2

import json

from sort.sort import Sort

from dataset.gram_rtm import GramDataset
from dataset.mio_tcd import MioDataset
from config.defaults import (
    MODELS,
    MASK_PATH,
    V5_GRAM_WEIGHTS_PATH,
    V5_MIO_WEIGHTS_PATH,
    V8_MIO_WEIGHTS_PATH,
    VIDEO_FORMAT,
    RESULTS_PATH
)


def get_video_list(folder_path: str) -> list:
    return sorted([f for f in os.listdir(folder_path) if f.endswith(VIDEO_FORMAT)])

def export_results(folder_path: str, name: str, data: list) -> None:
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, name + ".json"), 'w') as f:
       f.write(json.dumps(data))


def get_vehicles_position(yolo, tracker, frame):
    '''
    For frame get vehicles data applying yolo and sort
    '''

    boxes, classes, confs = yolo.detect_objects_in_frame(frame)
    if len(boxes) != 0:
        tracked_objects = tracker.update(boxes)
    else:
        return {}

    objects = {}
    for obj, cls, conf in zip(tracked_objects, classes, confs):
        x1, y1, x2, y2, obj_id = obj
        objects[obj_id] = {"id": obj_id, "class": cls, "bbox": [x1, y1, x2, y2], "conf": conf}

    return objects

def detect_video(video_path, yolo, mask, silent: bool = False) -> list:
    if not silent:
        print(f"Detecting {video_path}")

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    history = {}

    frame_number = 1
    while cap.isOpened():
        if not silent and frame_number % 120 == 0:
            print(f"{frame_number}/{total_frames}\t{frame_number // 120} s")
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        roi_frame = cv2.bitwise_and(frame, frame, mask=mask)
        history[frame_number] = get_vehicles_position(yolo, tracker, roi_frame)

        frame_number += 1

    cap.release()
    
    return history


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Missing arguments. Please use command:\ntrack_vehicles.py v5m_gram|v5m_mio|v8s_mio single_video|folder_path")
        exit(-1)
    if str(sys.argv[1]) not in MODELS:
        print("Unknow model: use v5m_gram|v5m_mio|v8s_mio")
    model_name = str(sys.argv[1])
    arg_2 = str(sys.argv[2])
    if os.path.isdir(arg_2):
        folder_path = arg_2
        video_list = get_video_list(folder_path)
    else:
        folder_path = os.path.dirname(arg_2)
        video_file = os.path.basename(arg_2)
        video_list = [video_file]
        
    # Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = os.path.join(RESULTS_PATH, "tracks", model_name + "_" + timestamp)
    print(f"Results in dir: {output_folder}")

    # Detect with selected model
    if model_name == MODELS[0]:
        ds = GramDataset()
        yolo = YOLO5(V5_GRAM_WEIGHTS_PATH, ds.VEHICLE_CLASSES)
        yolo.silence_warning()
    elif model_name == MODELS[1]:
        ds = MioDataset()
        yolo = YOLO5(V5_MIO_WEIGHTS_PATH, ds.VEHICLE_CLASSES)
        yolo.silence_warning()
    elif model_name == MODELS[2]:
        ds = MioDataset()
        yolo = YOLO8(V8_MIO_WEIGHTS_PATH, ds.VEHICLE_CLASSES)

    # Import tracker
    tracker = Sort()

    # Import mask
    roi_mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)
    mask = cv2.threshold(roi_mask, 127, 255, cv2.THRESH_BINARY)[1]
    
    # For each video detect and save results
    for video_file in video_list:
        video_path = os.path.join(folder_path, video_file)
        history = detect_video(video_path, yolo, mask=mask)

        export_results(output_folder, os.path.splitext(video_file)[0], history)
