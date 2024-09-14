# Installare YOLO v5 e YOLO v8

Esistono diversi modi per installare le diverse versioni di **YOLO** by Ultralytics. Le versioni principali utilizzate sono la versione 5 e la versione 8.


## Setup della versione 5

All'interno della cartella `detection/`, che sarà il workspace di YOLO v5, clonare il repository ufficiale:
```sh
git clone https://github.com/ultralytics/yolov5
```
Dopo aver preparato il virtual enviroment `.v5env` come descritto in questa ([guida](./CUDA%20on%20Windows.md)) all'interno della cartella `detection/`.
Installare le dipendenze mediante il comando
```sh
pip install -r yolov5/requirements.txt
```

Per controllare che tutto sia stato installato correttamente, e verificare il dispositivo su cui saranno eseguiti i calcoli (CPU o GPU) lanciare i comandi
```sh
./detection/.v5env/Scripts/activate
python ./detection/src/test/check_yolov5.py
```



## Setup della versione 8

Sempre all'interno della cartella `detection/`, creare il virtual enviroment `.v8env` all'interno della cartella `detection/`.
Dopo aver attivato l'enviroment, eseguire il comando
```sh
pip install ultralytics==8.0.196
```

Per controllare che tutto sia stato installato correttamente, e verificare il dispositivo su cui saranno eseguiti i calcoli (CPU o GPU) lanciare i comandi
```sh
./detection/.v8env/Scripts/activate
python ./detection/src/test/check_yolov8.py
```

