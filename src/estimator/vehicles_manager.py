from estimator.speed import centroid


def _get_last_seen_on_video(tracks: dict) -> dict:
    '''
    For each vehicle object, get last apparition frame
    '''
    last_seen = {}
    for frame, objects in tracks.items():
        for obj_id in objects.keys():
            last_seen[obj_id] = int(frame)
    return last_seen

def get_vehicles_dictionary(history: dict) -> dict:
    '''
    For each vehicle in history frames, get vehicle class, last bounding box, all positions (centered in bounding box) and frame associated.
    '''
    all_vehicles = {}
    for frame, objects in history.items():
        for vehicle_id, vehicle in objects.items():
            obj_center = centroid(vehicle['bbox'])
            cls = int(vehicle['class'])

            if vehicle_id not in all_vehicles:
                all_vehicles[vehicle_id] = {'class': cls, 'centers': {}}

            all_vehicles[vehicle_id]['centers'][int(frame)] = obj_center
            all_vehicles[vehicle_id]['bbox'] = vehicle['bbox']
    return all_vehicles

def drag_tracks(tracks: dict) -> dict:
    '''
    Construct a data structure to maintain a history of object locations from first apparition to last
    '''
    object_history = {}
    result_dict = {}
    last_seen = _get_last_seen_on_video(tracks)

    for frame, tracked_objects in tracks.items():
        frame = int(frame)
        result_dict[frame] = {}

        # Aggiorna o aggiungi i dati nel dizionario storico per ogni oggetto
        for obj_id, obj_data in tracked_objects.items():
            if obj_id not in object_history:
                # Crea un nuovo storico per l'oggetto se non esiste già
                object_history[obj_id] = {
                    "id": obj_data["id"],
                    "class": obj_data["class"],
                    "bbox": {},
                    "conf": obj_data["conf"]
                }
            
            # Aggiungi la posizione corrente al bbox per l'oggetto
            object_history[obj_id]["bbox"][frame] = obj_data["bbox"]

        # Copia gli oggetti attivi nel frame corrente nel dizionario dei risultati
        for obj_id in list(object_history.keys()):
            # Se l'oggetto non appare più nella scena, rimuovilo dallo storico
            if frame > last_seen[obj_id]:
                del object_history[obj_id]
                continue
            
            result_dict[frame][obj_id] = {
                "id": object_history[obj_id]["id"],
                "class": object_history[obj_id]["class"],
                "bbox": object_history[obj_id]["bbox"].copy(),
                "conf": object_history[obj_id]["conf"]
            }
                
    return result_dict

