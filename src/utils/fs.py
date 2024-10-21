import json
import csv

import os


def save_labels(output_file_path: str, labels: list):
    with open(output_file_path, 'w') as file:
        for item in labels:
            file.write(f"{item}\n")


def get_file_format_list(folder_path: str, format: str) -> list:
    return sorted([f for f in os.listdir(folder_path) if f.endswith(format)])


def get_tracking(tracking_path: str) -> dict:
    with open(tracking_path) as f:
        return json.load(f)

def export_speed_results(folder_path: str, name: str, header: list, data: list) -> None:
    with open(folder_path + name + ".csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)
