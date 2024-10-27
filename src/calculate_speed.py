from config.defaults import BENCHMARK_PATH, BENCHMARK_LABELS_FILE
from validator.benchmark import Benchmark
from estimator.speed import calculate_speed
from utils.fs import get_tracking, get_file_format_list, export_speed_results
from estimator.speed import calculate_speed

import os
import sys


def get_vehicles_dictionary(history: dict) -> dict:
    '''
    For each vehicle in history frames, get all positions (centered in bounding box) and frame associated.
    Remap centers to homography space
    '''
    all_vehicles = {}
    for frame, objects in history.items():
        for vehicle_id, vehicle in objects.items():
            x1, y1, x2, y2 = vehicle['bbox']
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            obj_center = (center_x, center_y)

            if vehicle_id not in all_vehicles:
                all_vehicles[vehicle_id] = {int(frame): obj_center}
            else:
                all_vehicles[vehicle_id][int(frame)] = obj_center
    return all_vehicles

def main(argv: list = []):
    input_folder = str(argv[1])
    output_folder = str(argv[2])

    results_list = get_file_format_list(input_folder, ".json")
    print(f"There are {len(results_list)} tracked videos")

    labels_path = os.path.join(BENCHMARK_PATH, BENCHMARK_LABELS_FILE)
    benchmark = Benchmark(labels_path)

    for video_file in results_list:
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        print(f"Processing {video_name}")
        video_tracks_path = os.path.join(input_folder, video_file)

        exporting_data = []
        history = get_tracking(video_tracks_path)
        all_vehicles = get_vehicles_dictionary(history)

        for vehicle_id, vehicle in all_vehicles.items():
            speed_estimation = calculate_speed(vehicle)
            if speed_estimation is None:
                continue

            benchmark_speed = benchmark.find_vehicle_speed(video_name, vehicle)
            min_f, max_f = benchmark.get_apparition_frames(vehicle)
            exporting_data.append([video_file.rsplit('.', 1)[0], min_f, max_f, speed_estimation, benchmark_speed])

        export_speed_results(output_folder, os.path.splitext(video_file)[0], ["File video", "min Frame", "max Frame", "calculated speed", "ground thrut"], exporting_data)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Missing arguments. Please use command:\ncalculate_speed.py input_folder_path outputh_folder_path")
        exit(-1)
    main(sys.argv)