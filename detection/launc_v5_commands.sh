# Selezionare dataset di interesse
dataset=mio|gram

# Inizia il learning
python src/yolov5/train.py --img 640 --batch 64 --epochs 30 --freeze 10 --data "detection/dataset_$dataset.yaml" --weights "yolov5m.pt" --project "detection/weights/yolo v5/$dataset"

# Continua il learning
python src/yolov5/train.py --resume --weights "detection/weights/yolo v5/$dataset/exp/weights/last.pt"

# Valida i risultati
python src/yolov5/val.py --img 640 --batch-size 64 --data "detection/dataset_$dataset.yaml" --weights "detection/weights/yolo v5/$dataset/exp/weights/best.pt"
