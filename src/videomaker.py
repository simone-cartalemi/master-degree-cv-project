import cv2

import os
from argparse import ArgumentParser

from dataset.gram_rtm import GramDataset
from dataset.mio_tcd import MioDataset
from config.defaults import RESULTS_PATH, TRACK_COLORS
from utils.fs import get_tracking
from estimator.speed import calculate_speed
from calculate_speed import get_vehicles_dictionary, centroid


def _get_last_seen_on_video(tracks: dict) -> dict:
    '''
    For each vehicle object, get last apparition frame
    '''
    last_seen = {}
    for frame, objects in tracks.items():
        for obj_id in objects.keys():
            last_seen[obj_id] = int(frame)
    return last_seen

def drag_tracks(tracks: dict) -> dict:
    '''
    Construct a data structure to maintain a history of object locations from first apparition to last
    '''
    object_history = {}
    result_dict = {}
    last_seen = _get_last_seen_on_video(tracks)

    for frame, tracked_objects in tracks.items():
        frame = int(frame)
        result_dict[frame] = {}

        # Aggiorna o aggiungi i dati nel dizionario storico per ogni oggetto
        for obj_id, obj_data in tracked_objects.items():
            if obj_id not in object_history:
                # Crea un nuovo storico per l'oggetto se non esiste già
                object_history[obj_id] = {
                    "id": obj_data["id"],
                    "class": obj_data["class"],
                    "bbox": {},
                    "conf": obj_data["conf"]
                }
            
            # Aggiungi la posizione corrente al bbox per l'oggetto
            object_history[obj_id]["bbox"][frame] = obj_data["bbox"]

        # Copia gli oggetti attivi nel frame corrente nel dizionario dei risultati
        for obj_id in list(object_history.keys()):
            # Se l'oggetto non appare più nella scena, rimuovilo dallo storico
            if frame > last_seen[obj_id]:
                del object_history[obj_id]
                continue
            
            result_dict[frame][obj_id] = {
                "id": object_history[obj_id]["id"],
                "class": object_history[obj_id]["class"],
                "bbox": object_history[obj_id]["bbox"].copy(),
                "conf": object_history[obj_id]["conf"]
            }
                
    return result_dict


def draw_tracks_video(video_path: str, history: dict, output_path: str, classes: list):
    video_name = os.path.basename(video_path)
    print(f"Making tracks on {video_name}")

    # Inizializza il lettore del video di input
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Inizializza il writer del video di output
    output_video_path = os.path.join(output_path, "tracks_" + video_name)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    all_vehicles = get_vehicles_dictionary(history)
    history = drag_tracks(history)

    frame_number = 1
    while cap.isOpened() and frame_number <= total_frames:
        if frame_number % 120 == 0:
            print(f"{frame_number}/{total_frames}\t{frame_number // 120} s")

        ret, frame = cap.read()
        if not ret:
            break

        for object_id, object_data in history[frame_number].items():
            c = TRACK_COLORS[int(float(object_id)) % len(TRACK_COLORS)]
            speed = calculate_speed(all_vehicles[object_id]['centers'])
            cls = classes[int(object_data["class"])]
            for bbox in object_data['bbox'].values():
                px, py = centroid(bbox)
                cv2.circle(frame, (int(px), int(py)), radius=3, color=c, thickness=-1)
            out_speed_text = f"Speed: {speed} km/h " if speed else ""
            if frame_number in object_data["bbox"]:
                x1, y1, x2, y2 = object_data["bbox"][frame_number]
            cv2.putText(frame, f"{out_speed_text}ID: {object_id}, Cls: {cls}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Scrivi il frame nel video
        out.write(frame)
        frame_number += 1

    # Rilascia il writer del video
    out.release()
    # Rilascia il lettore del video di input
    cap.release()

    print(f"File saved in {output_video_path}")

def draw_bndbox_video(video_path: str, history: dict, output_path: str, classes: list):
    video_name = os.path.basename(video_path)
    print(f"Making bounding box on {video_name}")

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


def main(video_file: str, video_tracks_path: str, dataset: str = "mio", draw_tracks: bool = False):
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

    if draw_tracks:
        draw_tracks_video(video_file, history, output_folder, classes)
    else:
        draw_bndbox_video(video_file, history, output_folder, classes)


# TODO: formato video come parametro

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("video_path", type=str, help="Path of input video")
    parser.add_argument("video_tracks_path", type=str, help="Path of video's tracks json file")
    parser.add_argument("-d", "--dataset", type=str, default="mio", help="Dataset mode")
    parser.add_argument("-t", "--tracks", action="store_true", help="Show vehicles track")

    args = parser.parse_args()

    if os.path.isdir(args.video_path):
        print("First argument must be a video file, not a folder")
    if os.path.isdir(args.video_tracks_path) or not args.video_tracks_path.lower().endswith('.json'):
        print("Please insert valid json file")

    main(args.video_path, args.video_tracks_path, args.dataset, args.tracks)
