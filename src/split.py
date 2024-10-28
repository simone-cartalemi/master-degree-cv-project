import os
import argparse
import shutil
import random
from pathlib import Path
from tqdm import tqdm


def split_dataset(dataset_path, train_ratio=0.8):
    # Percorsi alle sottocartelle
    images_dir = os.path.join(dataset_path, 'images')
    labels_dir = os.path.join(dataset_path, 'labels')

    # Creare sottocartelle per training e validation
    train_images_dir = os.path.join(images_dir, 'train')
    val_images_dir = os.path.join(images_dir, 'val')
    train_labels_dir = os.path.join(labels_dir, 'train')
    val_labels_dir = os.path.join(labels_dir, 'val')

    Path(train_images_dir).mkdir(parents=True, exist_ok=True)
    Path(val_images_dir).mkdir(parents=True, exist_ok=True)
    Path(train_labels_dir).mkdir(parents=True, exist_ok=True)
    Path(val_labels_dir).mkdir(parents=True, exist_ok=True)

    # Ottieni lista di tutti i file
    image_files = sorted(os.listdir(images_dir))
    label_files = sorted(os.listdir(labels_dir))

    # Filtra solo i file immagini e label escludendo le sottocartelle
    image_files = [f for f in image_files if os.path.isfile(os.path.join(images_dir, f))]
    label_files = [f for f in label_files if os.path.isfile(os.path.join(labels_dir, f))]

    # Assicurarsi che ogni immagine abbia una label corrispondente
    image_label_pairs = [(img, lbl) for img, lbl in zip(image_files, label_files) if img.rsplit('.', 1)[0] == lbl.rsplit('.', 1)[0]]

    # Mescola i dati
    random.shuffle(image_label_pairs)

    # Calcola il numero di file per il training set
    train_size = int(len(image_label_pairs) * train_ratio)

    # Divide tra training e validation
    train_pairs = image_label_pairs[:train_size]
    val_pairs = image_label_pairs[train_size:]

    # Copia i file nella cartella corrispondente
    print(f"{len(train_pairs)} in train")
    for img_file, lbl_file in tqdm(train_pairs):
        shutil.move(os.path.join(images_dir, img_file), os.path.join(train_images_dir, img_file))
        shutil.move(os.path.join(labels_dir, lbl_file), os.path.join(train_labels_dir, lbl_file))

    print(f"{len(val_pairs)} in val")
    for img_file, lbl_file in tqdm(val_pairs):
        shutil.move(os.path.join(images_dir, img_file), os.path.join(val_images_dir, img_file))
        shutil.move(os.path.join(labels_dir, lbl_file), os.path.join(val_labels_dir, lbl_file))


def main(full_data_path: str, ratio: float = 0.8):
    split_dataset(full_data_path, train_ratio=ratio)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("full_data_path", type=str, help="Dataset: gram|mio")
    parser.add_argument("ratio", type=float, default=0.8, help="All dataset images folder")

    args = parser.parse_args()
    main(args.full_data_path, args.ratio)
