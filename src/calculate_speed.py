import os
from argparse import ArgumentParser

from validator.benchmark import Benchmark
from config.defaults import BENCHMARK_LABELS_FILE, BENCHMARK_PATH
from estimator.speed import linear_speed
from estimator.vehicles_manager import get_vehicles_dictionary
from utils.fs import export_csv_lines, get_file_format_list, get_tracking


def main(input_folder: str, output_folder: str, benchmarking_labels: bool = False):
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

        for vehicle in all_vehicles.values():
            vehicle_centers = vehicle['centers']
            vehicle_class = vehicle['class']
            speed_estimation = linear_speed(vehicle_centers)
            if speed_estimation is None:
                continue

            benchmark_speed = benchmark.find_vehicle_speed(video_name, vehicle_centers) if benchmarking_labels else ""
            min_f, max_f = benchmark.get_apparition_frames(vehicle_centers)
            exporting_data.append([video_file.rsplit('.', 1)[0], min_f, max_f, vehicle_class, speed_estimation, benchmark_speed])

        export_csv_lines(output_folder, os.path.splitext(video_file)[0], ["File video", "min Frame", "max Frame", "vehicle class", "calculated speed", "ground thrut"], exporting_data)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_folder_path", type=str, help="Path of videos' track json file")
    parser.add_argument("output_folder_path", type=str, help="Path of output folder")
    parser.add_argument("-b", "--benchmark", action="store_true", help="Add benchmarking to results")

    args = parser.parse_args()

    main(args.input_folder_path, args.output_folder_path, args.benchmark)
