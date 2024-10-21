import json

def get_tracking(tracking_path: str) -> dict:
    with open(tracking_path) as f:
        return json.load(f)
