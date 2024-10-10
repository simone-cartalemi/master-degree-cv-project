dataset=mio|gram

# Inizia il learning
python detection/yolov5/train.py --img 640 --batch 16 --epochs 20 --freeze 10 --data "detection/src/dataset_$dataset.yaml" --project detection/weights/

# Continua il learning
python detection/yolov5/train.py --img 640 --batch 16 --epochs 20 --freeze 10 --data "detection/src/dataset_$dataset.yaml" --weights detection/weights/exp1/weights/best.pt --project detection/weights/
