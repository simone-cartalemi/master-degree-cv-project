import cv2
import matplotlib.pyplot as plt

import os
import sys



if __name__ == "__main__":
    img_folder_path = str(sys.argv[1])
    index_img = int(sys.argv[2])
    label_path = os.path.join(img_folder_path, "../labels/")


    imgs = [f for f in os.listdir(img_folder_path) if os.path.isfile(os.path.join(img_folder_path, f))]
    imgs.sort()

    img_name = imgs[index_img]
    img_path = os.path.join(img_folder_path, img_name)
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    img_height, img_width, layers = img.shape
    print(f"Le dimensioni dell'immagine sono {img_width}x{img_height}")


    with open(os.path.join(label_path, img_name.replace(".jpg", ".txt"))) as file:
        lines = [line.rstrip() for line in file]
    print("Ci sono", len(lines), "oggetti")
    for line in lines:
        cls, c_x, c_y, w, h = line.split(' ')

        abs_w = img_width * float(w)
        abs_h = img_height * float(h)
        x1 = float(c_x) * img_width - abs_w / 2
        y1 = float(c_y) * img_height - abs_h / 2
        x2 = float(c_x) * img_width + abs_w / 2
        y2 = float(c_y) * img_height + abs_h / 2
        
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, f"Classe: {cls}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    plt.imshow(img)
    plt.axis('off')
    plt.show()
