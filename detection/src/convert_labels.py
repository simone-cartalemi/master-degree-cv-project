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

    def compose_name(self, annotation_name):
        '''
        Costruisce il nome dell'immagine a partire dal nome del file xml di annotazione.
        Nota che il file 0.xml corrisponde al file image000001.jpg
        '''

        img_name = annotation_name.replace('.xml', '')
        img_name = str(int(img_name) + 1)
        name = "image000000"
        return name[:-len(img_name)] + img_name

    def get_labels(self, labels_path):
        '''
        Prende il path di una cartella che contiene file xml di annotazioni e restituisce un dict del tipo {"img": [obj]}
        '''

        if not os.path.isdir(labels_path):
            raise "Path label per dataset GRAM-RTM non corretto"
        
        annotation_paths = sorted([f for f in os.listdir(labels_path) if f.lower().endswith('.xml')])

        labels_data = {}
        for annotations in annotation_paths:
            img_name = self.compose_name(annotations)
            labels_data[img_name] = self.read_xml(os.path.join(labels_path, annotations))
        
        return labels_data



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

def save_labels(output_file_path, labels):
    with open(output_file_path, 'w') as file:
        for item in labels:
            file.write(f"{item}\n")




if __name__ == "__main__":
    dataset_name = str(sys.argv[1])
    images_folder_path = str(sys.argv[2])
    labels_path = str(sys.argv[3])
    labels_out_path = os.path.join(images_folder_path, "../labels/")
    os.makedirs(labels_out_path, exist_ok=True)

    Ds = None
    if dataset_name == "mio-tcd":
        Ds = MioDataset()
    elif dataset_name == "gram":
        Ds = GramDataset()
    else:
        raise "Nome dataset sconosciuto"
    
    labels = Ds.get_labels(labels_path)
    for img_name, objs in tqdm(labels.items()):
        img_path = os.path.join(images_folder_path, img_name + '.jpg')

        if not os.path.isfile(img_path):
            continue
    
        new_labels_path = os.path.join(labels_out_path, img_name + '.txt')
        new_labels = yolo_format(img_path, objs)
        save_labels(new_labels_path, new_labels)
