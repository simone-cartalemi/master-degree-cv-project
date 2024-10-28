import cv2

import os
import argparse

from dataset.gram_rtm import GramDataset
from dataset.mio_tcd import MioDataset
from config.defaults import RESULTS_PATH
from utils.fs import get_tracking


def draw_bndbox_video(video_path: str, history: dict, output_path: str, classes: list):
    video_name = os.path.basename(video_path)
    print(f"Making tracks on {video_name}")

    # Video data
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Writer video
    output_video_path = os.path.join(output_path, "bnd-box_" + video_name)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')    # cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    frame_number = 1
    while cap.isOpened():
        if frame_number % 120 == 0:
            print(f"{frame_number}/{total_frames}\t{frame_number // 120} s")
        ret, frame = cap.read()
        if not ret:
            break

        # Draw bounding box, ID and classe on frame
        for obj in history[str(frame_number)].values():
            x1, y1, x2, y2 = obj["bbox"]
            obj_id = obj["id"]
            cls = classes[int(obj["class"])]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {int(obj_id)}, Cls: {cls}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Add the frame on video
        out.write(frame)

        frame_number += 1

    cap.release()

    # Leave writer
    out.release()
    print(f"File saved in {output_video_path}")


def main(video_tracks_path: str, video_file: str, dataset: str = "mio", draw_tracks: bool = False):
    # Get class label
    if dataset == "gram":
        ds = GramDataset()
    else:
        ds = MioDataset()
    classes = list(ds.VEHICLE_CLASSES.keys())
    
    # Get tracking data
    history = get_tracking(video_tracks_path)

    output_folder = os.path.join(RESULTS_PATH, "tracks/videos/")
    os.makedirs(output_folder, exist_ok=True)
    draw_bndbox_video(video_file, history, output_folder, classes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", type=str, help="Path of input video")
    parser.add_argument("video_tracks_path", type=str, help="Path of video's tracks json file")
    parser.add_argument("-d", "--dataset", type=str, default="mio", help="Dataset mode")
    parser.add_argument("-t", "--tracks", action="store_true", help="Show vehicles track")

    args = parser.parse_args()

    if os.path.isdir(args.video_tracks_path) or not args.video_tracks_path.lower().endswith('.json'):
        print("Please insert valid json file")
    if os.path.isdir(args.video_path):
        print("First argument must be a video file, not a folder")

    main(args.video_tracks_path, args.video_path, args.dataset, args.tracks)
