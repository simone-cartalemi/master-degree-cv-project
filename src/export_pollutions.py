import os
from argparse import ArgumentParser

from config.defaults import RESULTS_PATH
from estimator.pollution import rearrange_speed_results, pollution_trend
from util.fs import export_csv_lines, get_csv_lines, get_file_format_list


def main(resource_path: str, verbose: bool = False) -> str:
    if os.path.isdir(resource_path):
        folder_path = resource_path + "/"
        speed_result_list = get_file_format_list(folder_path, ".csv")
    else:
        folder_path = os.path.dirname(resource_path) + "/"
        speed_result_file_name = os.path.basename(resource_path)
        speed_result_list = [speed_result_file_name]

    output_folder = os.path.join(RESULTS_PATH, "pollution", os.path.basename(os.path.dirname(folder_path)))

    for video_file in speed_result_list:
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        if verbose:
            print(f"Exporting pollution results in {video_file}")

        result_path = os.path.join(folder_path, video_file)
        results = get_csv_lines(result_path)
        all_estimation_data = rearrange_speed_results(results)
        cumulative_pollution = pollution_trend(all_estimation_data.get(video_name, []))

        export_csv_lines(output_folder, video_name, ["vehicle in frame", "frame pollution"], cumulative_pollution)

    return output_folder


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("resource_path", type=str, help="Path of input video or videos' folder")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print output")

    args = parser.parse_args()
    main(args.resource_path, args.verbose)
