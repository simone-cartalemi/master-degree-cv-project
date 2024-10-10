
# Inizia il learning
yolo task=detect mode=train model=yolov8s.pt data=detection/src/dataset_mio.yaml batch=64 epochs=30 imgsz=640 plots=True project="detection/weights/yolo v8"

# Continua il learning
yolo train resume model="detection/weights/yolo v8/train/weights/best.pt"


# Valida il modello
yolo task=detect mode=val model="detection/weights/yolo v8/train/weights/best.pt" data=detection/src/dataset_mio.yaml
