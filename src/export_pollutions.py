import os
from argparse import ArgumentParser

from estimator.pollution import rearrange_speed_results, pollution_trend
from util.fs import export_csv_lines, get_csv_lines, get_file_format_list


def main(resource_path: str, output_folder: str, verbose: bool = False):
    if os.path.isdir(resource_path):
        folder_path = resource_path
        speed_result_list = get_file_format_list(folder_path, ".csv")
    else:
        folder_path = os.path.dirname(resource_path)
        speed_result_file_name = os.path.basename(resource_path)
        speed_result_list = [speed_result_file_name]

    for speed_result_file in speed_result_list:
        video_name = speed_result_file.rsplit('.', 1)[0]
        if verbose:
            print(f"Exporting pollution results in {speed_result_file}")

        result_path = os.path.join(folder_path, speed_result_file)
        results = get_csv_lines(result_path)
        all_estimation_data = rearrange_speed_results(results)
        cumulative_pollution = pollution_trend(all_estimation_data[video_name])

        export_csv_lines(output_folder, video_name, ["vehicle in frame", "frame pollution"], cumulative_pollution)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("resource_path", type=str, help="Path of input video or videos' folder")
    parser.add_argument("output_folder_path", type=str, help="Path of output folder")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print output")

    args = parser.parse_args()
    main(args.resource_path, args.output_folder_path, args.verbose)
