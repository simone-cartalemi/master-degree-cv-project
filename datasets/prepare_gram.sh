#!/bin/sh

# Scarica l'archivio zip principale ed estrailo
wget -O ./datasets/GRAM-RTMv4.zip -l 1 "https://gram.web.uah.es/data/datasets/rtm/GRAM-RTMv4.zip"
unzip ./datasets/GRAM-RTMv4.zip -d datasets/

# Scarica i tre dataset
wget -O ./datasets/GRAM-RTMv4/M-30.zip -l 1 "https://universidaddealcala-my.sharepoint.com/:u:/g/personal/gram_uah_es/EZueCuaiFVZKlZZGRcJxpasB2xnaxDPm2MIKi9LQHROSMA?&Download=1"
wget -O ./datasets/GRAM-RTMv4/M-30-HD.zip -l 1 "https://universidaddealcala-my.sharepoint.com/:u:/g/personal/gram_uah_es/ERVzfHbeq6JEplBycRHF6akBj4_9j6_hAKzCNVT6fKO0ug?&Download=1"
wget -O ./datasets/GRAM-RTMv4/Urban1.zip -l 1 "https://universidaddealcala-my.sharepoint.com/:u:/g/personal/gram_uah_es/ERLovJRNvDBIpGihNS_5jWcBRioD8ib_mTTPFDXqyc84PA?&Download=1"

# Definisci array dei tre dataset
dataset_names=("M-30" "M-30-HD" "Urban1")

# Estrai i tre archivi
for dataset_name in "${dataset_names[@]}"; do
    unzip ./datasets/GRAM-RTMv4/"$dataset_name".zip -d ./datasets/GRAM-RTMv4/Images/
done

# Sposta gli archivi zip in un altra cartella
mkdir ./datasets/GRAM-RTMv4/Archives
mv ./datasets/GRAM-RTMv4.zip ./datasets/GRAM-RTMv4/Archives
for dataset_name in "${dataset_names[@]}"; do
    mv ./datasets/GRAM-RTMv4/"$dataset_name".zip ./datasets/GRAM-RTMv4/Archives
done

# Riorganizza le cartelle
for dataset_name in "${dataset_names[@]}"; do
    mv ./datasets/GRAM-RTMv4/Images/"$dataset_name"/ ./datasets/GRAM-RTMv4/Images/images/
    mkdir ./datasets/GRAM-RTMv4/Images/"$dataset_name"/
    mv ./datasets/GRAM-RTMv4/Images/images/ ./datasets/GRAM-RTMv4/Images/"$dataset_name"/images/
done

# Esegui labeling e splitting
for dataset_name in "${dataset_names[@]}"; do
    python ./detection/src/convert_labels.py gram ./datasets/GRAM-RTMv4/Images/"$dataset_name"/images/ ./datasets/GRAM-RTMv4/Annotations/"$dataset_name"/xml/
    python ./detection/src/split.py ./datasets/GRAM-RTMv4/Images/"$dataset_name"/ 0.8
done
