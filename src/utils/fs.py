import json
import csv

import os


def save_labels(output_file_path: str, labels: list):
    with open(output_file_path, 'w') as file:
        for item in labels:
            file.write(f"{item}\n")


def get_file_format_list(folder_path: str, format: str) -> list:
    return sorted([f for f in os.listdir(folder_path) if f.endswith(format)])

def get_csv_lines(csv_file_path: str) -> list:
    rows = []
    with open(csv_file_path, mode ='r') as f:
        csvFile = csv.reader(f)
        next(csvFile)
        for row in csvFile:
            rows.append(row)
    return rows

def export_tracking_results(folder_path: str, name: str, data: list) -> None:
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, name + ".json"), 'w') as f:
       f.write(json.dumps(data))

def get_tracking(tracking_path: str) -> dict:
    with open(tracking_path) as f:
        return json.load(f)


def export_speed_results(folder_path: str, name: str, header: list, data: list) -> None:
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, name + ".csv"), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)
