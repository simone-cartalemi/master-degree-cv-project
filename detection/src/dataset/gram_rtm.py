from dataset.dataset import Dataset

import os
import xml.etree.ElementTree as ET


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
            elif cls == "bus":
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
