import csv

from config.defaults import VALIDATION_WINDOW


class Benchmark():
    ground_truth = {}

    def __init__(self, file_path: str) -> None:
        with open(file_path, mode ='r') as f:
            csvFile = csv.reader(f)
            next(csvFile)
            for lines in csvFile:
                video_name, frame_n, id_vehicle, laser_speed = lines
                if video_name not in self.ground_truth:
                    self.ground_truth[video_name] = {int(frame_n): int(laser_speed)}
                else:
                    self.ground_truth[video_name][int(frame_n)] = int(laser_speed)

    def get_apparition_frames(self, vehicle_history: dict) -> tuple:
        return ( min(vehicle_history.keys()), max(vehicle_history.keys()) )

    def find_vehicle_speed(self, name_video: str, vehicle_history: dict, frame_error_range: int = 10) -> int|None:
        '''
        Check if the vehicle history matches the benchmark history (must be at the same place in the same frame number)
        '''
        gt_video = self.ground_truth[name_video]
        if not len(gt_video):
            return None
        min_vehicle_f, max_vehicle_f = self.get_apparition_frames(vehicle_history)
        
        frame_target_candidates = [f for f in gt_video.keys() if f >= min_vehicle_f and f <= max_vehicle_f]
        for f_t in frame_target_candidates:
            for f_i in range(f_t - frame_error_range, f_t + frame_error_range):
                if f_i in vehicle_history and vehicle_history[f_i][1] >= VALIDATION_WINDOW[0] and vehicle_history[f_i][1] <= VALIDATION_WINDOW[1]:
                    return gt_video.pop(f_t)
        return None
