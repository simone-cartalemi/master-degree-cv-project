import cv2
import os
import sys
from tqdm import tqdm

from dataset.gram_rtm import GramDataset
from dataset.mio_tcd import MioDataset


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
