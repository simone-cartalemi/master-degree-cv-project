import sys
sys.path.append("src")

from src.track_vehicles import main as track_vehicles
from src.calculate_speed import main as calculate_speed
from src.export_pollutions import main as export_pollutions
from src.videomaker import main as videomaker
from src.track_vehicles import Model


video_path = "./datasets/thai/Videos/IMG_0606.MOV"

output_folder = track_vehicles(video_path, Model.V8_MIO, folder_name="")
output_folder = calculate_speed(output_folder, benchmarking_labels=True, verbose=True)
output_folder = export_pollutions(output_folder, verbose=True)

videomaker(video_path, output_folder + "/IMG_0606.json", draw_bndbox=True, draw_tracks=True, verbose=True)

