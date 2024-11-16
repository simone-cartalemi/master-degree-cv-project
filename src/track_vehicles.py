import datetime
import os
from argparse import ArgumentParser

import cv2
from sort.sort import Sort

from architectures.yolo_v5m import YOLO5
from architectures.yolo_v8s import YOLO8
from config.defaults import (
    Model,
    MASK_PATH,
    V5_GRAM_WEIGHTS_PATH,
    V5_MIO_WEIGHTS_PATH,
    V8_MIO_WEIGHTS_PATH,
    VIDEO_FORMAT,
    RESULTS_PATH
)
from dataset.gram_rtm import GramDataset
from dataset.mio_tcd import MioDataset
from util.fs import export_tracking_results, get_file_format_list


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

def detect_video(video_path, yolo, mask, verbose: bool) -> list:
    
    if verbose:
        print(f"Detecting {video_path}")

    # Import tracker
    tracker = Sort()

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    history = {}

    frame_number = 1
    while cap.isOpened():
        if verbose and frame_number % 120 == 0:
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


def main(resource_path: str, model: str, verbose: bool = False) -> str:
    if os.path.isdir(resource_path):
        folder_path = resource_path
        video_list = get_file_format_list(folder_path, VIDEO_FORMAT)
    else:
        folder_path = os.path.dirname(resource_path)
        video_file = os.path.basename(resource_path)
        video_list = [video_file]

    # Timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = os.path.join(RESULTS_PATH, "tracks", str(model) + "_" + timestamp)
    print(f"Results in dir: {output_folder}")

    # Detect with selected model
    if model == Model.V5_GRAM:
        ds = GramDataset()
        yolo = YOLO5(V5_GRAM_WEIGHTS_PATH, ds.VEHICLE_CLASSES)
        yolo.silence_warning()
    elif model == Model.V5_MIO:
        ds = MioDataset()
        yolo = YOLO5(V5_MIO_WEIGHTS_PATH, ds.VEHICLE_CLASSES)
        yolo.silence_warning()
    elif model == Model.V8_MIO:
        ds = MioDataset()
        yolo = YOLO8(V8_MIO_WEIGHTS_PATH, ds.VEHICLE_CLASSES)

    # Import mask
    roi_mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)
    mask = cv2.threshold(roi_mask, 127, 255, cv2.THRESH_BINARY)[1]
    
    # For each video detect and save results
    for video_file in video_list:
        video_path = os.path.join(folder_path, video_file)
        history = detect_video(video_path, yolo, mask, verbose)

        export_tracking_results(output_folder, os.path.splitext(video_file)[0], history)

    return output_folder


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("model", type=Model, choices=list(Model), help="Model name for detecting")
    parser.add_argument("resource_path", type=str, help="Path of input video or videos' folder")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print output")

    args = parser.parse_args()
    main(args.resource_path, args.model, args.verbose)
