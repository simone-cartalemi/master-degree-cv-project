import cv2
import os
import sys
import csv
from tqdm import tqdm

from abc import ABC, abstractmethod

import xml.etree.ElementTree as ET


class Dataset(ABC):
    VEHICLE_CLASSES = {}

    @abstractmethod
    def get_labels(self, labels_path):
        raise NotImplementedError("Il metodo load_labels deve essere implementato nelle sottoclassi")


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


class GramDataset(Dataset):

    VEHICLE_CLASSES = {"car": 0, "motorcycle": 1, "truck": 2, "van": 3}

    def read_xml(self, xml_path):
        '''
        Prende il path di un file xml di annotazioni e restituisce un array di dict del tipo obj}
        '''

        tree = ET.parse(xml_path)
        root = tree.getroot()
        objs = []
        for child in root.iter('object'):
            obj = {}
            cls = child.find("class").text
            if cls in self.VEHICLE_CLASSES:
                obj["class"] = self.VEHICLE_CLASSES[cls]
            elif cls == "motorbike":
                obj["class"] = self.VEHICLE_CLASSES["motorcycle"]
            elif cls == "big-truck":
                obj["class"] = self.VEHICLE_CLASSES["truck"]
            else:
                print("Classe non prevista:", cls)
            obj["id"] = child.find("ID").text

            bndbox = child.find('bndbox')

            x1 = int(bndbox.find("xmin").text)
            y1 = int(bndbox.find("ymin").text)
            x2 = int(bndbox.find("xmax").text)
            y2 = int(bndbox.find("ymax").text)
            obj["bndbox"] = [x1, y1, x2, y2]
            
            objs.append(obj)

        return objs

    def _get_labels(self, labels_path):
        '''
        Prende il path di una cartella che contiene file xml di annotazioni e restituisce un dict del tipo {"img": [obj]}
        '''

        annotation_paths = sorted([f for f in os.listdir(labels_path) if f.lower().endswith('.xml')])

        labels_data = {}
        for annotations in annotation_paths:
            img_name = annotations.replace('.xml', '')
            labels_data[img_name] = self.read_xml(annotations)
        
        return labels_data
        




    def altra(self, labels_path):
        for frame, label in tqdm(zip(frames, annotations)):
            name = frame.replace(".jpg", ".txt")
            objs = read_csv_data(ds_annotations + label)
            output_objects = []
            for obj in objs:
                cls_index = list(vehicle_classes.values()).index(obj["class"])
                cls = list(vehicle_classes.keys())[cls_index]
                x_center = ((obj["bndbox"][0] + obj["bndbox"][2]) / 2) / frame_width
                y_center = ((obj["bndbox"][1] + obj["bndbox"][3]) / 2) / frame_height
                width = (obj["bndbox"][2] - obj["bndbox"][0]) / frame_width
                height = (obj["bndbox"][3] - obj["bndbox"][1]) / frame_height
                output_objects.append(f"{vehicle_classes[cls]} {x_center} {y_center} {width} {height}")
            with open(input_folder + "labels/" + name, 'w') as file:
                for item in output_objects:
                    file.write(f"{item}\n")

    def load_labels(self, labels_file):
        tree = ET.parse(labels_file)
        root = tree.getroot()
        bbox = []
        for child in root.iter('object'):
            obj = {}
            cls = child.find("class").text
            if cls in self.VEHICLE_CLASSES:
                obj["class"] = self.VEHICLE_CLASSES[cls]
            elif cls == "motorbike":
                obj["class"] = 1
            elif cls == "big-truck":
                obj["class"] = 2
            else:
                print("Classe non prevista:", cls)
            obj["id"] = child.find("ID").text

            bndbox = child.find('bndbox')

            x1 = int(bndbox.find("xmin").text)
            y1 = int(bndbox.find("ymin").text)
            x2 = int(bndbox.find("xmax").text)
            y2 = int(bndbox.find("ymax").text)
            obj["bndbox"] = (x1, y1, x2, y2)
            
            bbox.append(obj)

        return bbox



def save_labels(output_file_path, annotations):
    with open(output_file_path, 'w') as file:
        for item in annotations:
            file.write(f"{item}\n")



def yolo_format(image_path, objs):
    img = cv2.imread(image_path)
    img_height, img_width, layers = img.shape

    output_objects = []
    for obj in objs:
        cls = obj["class"]
        x_center = ((obj["bndbox"][0] + obj["bndbox"][2]) / 2) / img_width
        y_center = ((obj["bndbox"][1] + obj["bndbox"][3]) / 2) / img_height
        width = (obj["bndbox"][2] - obj["bndbox"][0]) / img_width
        height = (obj["bndbox"][3] - obj["bndbox"][1]) / img_height
        output_objects.append(f"{cls} {x_center} {y_center} {width} {height}")
    return output_objects


if __name__ == "__main__":
    full_data_path = int(sys.argv[1])
    images_path = os.path.join(full_data_path, "/dataset/train/images/")
    labels_path = os.path.join(full_data_path, "gt_train.csv")
    labels_out_path = os.path.join(full_data_path, "/dataset/train/labels/")
    os.makedirs(labels_out_path, exist_ok=True)

    labels_data = load_mio_labels(labels_path, VEHICLE_CLASSES_MIO)

    # Ottieni la lista delle immagini
    images = sorted([f for f in os.listdir(images_path) if f.lower().endswith('.jpg')])

    for image in tqdm(images):
        labels_file_name = image.replace('.jpg', '.txt')
        
        converted = yolo_format(images_path + image, labels_data[image.replace('.jpg', '')])

        save_labels(labels_out_path + labels_file_name, converted)
