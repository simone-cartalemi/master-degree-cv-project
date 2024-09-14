import cv2
import os
import sys
import csv
from tqdm import tqdm


vehicle_classes = {
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


def load_labels(labels_path):
    labels_data = {}
    with open(labels_path, mode ='r') as f:
        csvFile = csv.reader(f)
        for lines in csvFile:
            img_name, class_name, x1, y1, x2, y2 = lines
            if img_name in labels_data:
                labels_data[img_name].append({"class": vehicle_classes[class_name], "bndbox": [int(x1), int(y1), int(x2), int(y2)]})
            else:
                labels_data[img_name] = [{"class": vehicle_classes[class_name], "bndbox": [int(x1), int(y1), int(x2), int(y2)]}]
    return labels_data

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

    labels_data = load_labels(labels_path)

    # Ottieni la lista delle immagini
    images = sorted([f for f in os.listdir(images_path) if f.lower().endswith('.jpg')])

    for image in tqdm(images):
        labels_file_name = image.replace('.jpg', '.txt')
        
        converted = yolo_format(images_path + image, labels_data[image.replace('.jpg', '')])

        save_labels(labels_out_path + labels_file_name, converted)
