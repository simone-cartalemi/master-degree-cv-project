#!/bin/sh

# Scarica l'archivio tar ed estrailo
curl -L "https://tcd.miovision.com/static/dataset/MIO-TCD-Localization.tar" -o ./datasets/MIO-TCD-Localization.tar
tar -xvf ./datasets/MIO-TCD-Localization.tar -C datasets/

# Sposta l'archivio in un altra cartella
mv ./datasets/MIO-TCD-Localization.tar ./datasets/MIO-TCD-Localization/

# Rinomina la cartella delle immagini
mv ./datasets/MIO-TCD-Localization/train ./datasets/MIO-TCD-Localization/images

# Esegui labeling e splitting
python ./src/convert_labels.py mio-tcd ./datasets/MIO-TCD-Localization/images/ ./datasets/MIO-TCD-Localization/gt_train.csv
python ./src/split.py ./datasets/MIO-TCD-Localization/ 0.8
