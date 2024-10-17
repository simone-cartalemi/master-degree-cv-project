from dataset.dataset import Dataset

import csv


class MioDataset(Dataset):

    VEHICLE_CLASSES = {
        'articulated_truck': 0,
        'bicycle': 1,
        'bus': 2,
        'car': 3,
        'motorcycle': 4,
        'motorized_vehicle': 5,
        'non-motorized_vehicle': 6,
        'pedestrian': 7,
        'pickup_truck': 8,
        'single_unit_truck': 9,
        'work_van': 10
    }

    def get_labels(self, labels_path):
        '''
        Prende il path di gt_train.csv in input e restituisce un dict del tipo {"img": [obj]}
        '''

        if not labels_path.lower().endswith('.csv'):
            raise "File label per dataset MIO-TCD non corretto"
        
        labels_data = {}
        with open(labels_path, mode ='r') as f:
            csvFile = csv.reader(f)
            for lines in csvFile:
                img_name, class_name, x1, y1, x2, y2 = lines
                if img_name in labels_data:
                    labels_data[img_name].append({"class": self.VEHICLE_CLASSES[class_name], "bndbox": [int(x1), int(y1), int(x2), int(y2)]})
                else:
                    labels_data[img_name] = [{"class": self.VEHICLE_CLASSES[class_name], "bndbox": [int(x1), int(y1), int(x2), int(y2)]}]
        return labels_data
