import os
from argparse import ArgumentParser

import cv2

from config.defaults import RESULTS_PATH, TRACK_COLORS
from dataset.gram_rtm import GramDataset
from dataset.mio_tcd import MioDataset
from estimator.vehicles_manager import drag_tracks, get_vehicles_dictionary
from estimator.speed import centroid, linear_speed
from utils.fs import get_tracking


def draw_in_video(
        video_path: str,
        history: dict,
        output_path: str,
        classes: list,
        draw_labels: bool,
        draw_bndbox: bool,
        draw_tracks: bool
):
    video_name = os.path.basename(video_path)
    print(f"Processing and exporting: {video_name}")

    # Process vehicles data
    all_vehicles = get_vehicles_dictionary(history)
    history = drag_tracks(history)

    # Initialize reader input video
    video_reader = cv2.VideoCapture(video_path)
    total_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video_reader.get(cv2.CAP_PROP_FPS)
    width  = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize writer output video
    output_video_path = os.path.join(output_path, "exporting_" + video_name)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    frame_number = 1
    while video_reader.isOpened() and frame_number <= total_frames:
        if frame_number % 120 == 0:
            print(f"{frame_number}/{total_frames}\t{frame_number // 120} s")

        ret, frame = video_reader.read()
        if not ret:
            break

        for object_id, object_data in history[frame_number].items():
            if frame_number in object_data["bbox"]:
                x1, y1, x2, y2 = object_data["bbox"][frame_number]
            if draw_tracks:
                c = TRACK_COLORS[int(float(object_id)) % len(TRACK_COLORS)]
                for bbox in object_data['bbox'].values():
                    px, py = centroid(bbox)
                    cv2.circle(frame, (int(px), int(py)), radius=3, color=c, thickness=-1)
            if draw_bndbox:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            if draw_labels:
                cls = classes[int(object_data["class"])]
                speed = linear_speed(all_vehicles[object_id]['centers'])
                out_speed_text = f"Speed: {speed} km/h " if speed else ""
                cv2.putText(frame, f"{out_speed_text}ID: {object_id}, Cls: {cls}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Write frame in video
        video_writer.write(frame)
        frame_number += 1

    # Release writer and reader
    video_writer.release()
    video_reader.release()

    print(f"File saved in {output_video_path}")


def main(
        video_path: str,
        video_tracks_path: str,
        dataset: str = "mio",
        draw_labels: bool = True,
        draw_bndbox: bool = False,
        draw_tracks: bool = False
):
    if os.path.isdir(video_path):
        print("First argument must be a video file, not a folder")
        return
    if os.path.isdir(video_tracks_path) or not video_tracks_path.lower().endswith('.json'):
        print("Please insert valid json file")
        return
    if not draw_labels and draw_bndbox and draw_tracks:
        print("Output video settings are nonsense")
        return

    # Get class label
    if dataset == "gram":
        ds = GramDataset()
    else:
        ds = MioDataset()
    classes = list(ds.VEHICLE_CLASSES.keys())
    
    # Get tracking data
    history = get_tracking(video_tracks_path)

    output_folder = os.path.join(RESULTS_PATH, "videos/")
    os.makedirs(output_folder, exist_ok=True)

    draw_in_video(video_path, history, output_folder, classes, draw_labels, draw_bndbox, draw_tracks)


# TODO: verbose parametro

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("video_path", type=str, help="Path of input video")
    parser.add_argument("video_tracks_path", type=str, help="Path of video's tracks json file")
    parser.add_argument("-d", "--dataset", type=str, default="mio", help="Dataset mode")
    parser.add_argument("-t", "--tracks", action="store_true", help="Show vehicles track")
    parser.add_argument("-b", "--bnd-box", action="store_true", help="Show vehicles bounding box")
    parser.add_argument("-nl", "--no-labels", action="store_false", help="Hide vehicles details")

    args = parser.parse_args()

    main(args.video_path, args.video_tracks_path, args.dataset, args.labels, args.bndbox, args.tracks)
