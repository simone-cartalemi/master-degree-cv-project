# Installare YOLO v5 e YOLO v8

Esistono diversi modi per installare le diverse versioni di **YOLO** by Ultralytics. Le versioni principali utilizzate sono la versione 5 e la versione 8.


## Setup della versione 5

All'interno della cartella `detection/`, che sarà il workspace di YOLO v5, clonare il repository ufficiale:
```sh
git clone https://github.com/ultralytics/yolov5
```
Dopo aver preparato il virtual enviroment `.v5env` come descritto in questa ([guida](./CUDA%20on%20Windows.md)) all'interno della cartella `detection/`,
installare le dipendenze mediante il comando
```sh
pip install -r yolov5/requirements.txt
```


