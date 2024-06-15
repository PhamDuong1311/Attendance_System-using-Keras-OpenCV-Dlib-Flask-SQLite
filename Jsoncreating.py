import json
import os
import numpy as np
import embedded_model
import cv2


def create_json_file(name, Id ,vector):
    eb = []
    data = {
        "name": name,
        "Id": Id,
        "vector": vector
    }

    file_name = os.path.join('data', f"{name}.json")
    
    # Lưu trữ dữ liệu vào tệp JSON
    with open(file_name, 'w') as file:
        json.dump(data, file)
        
def count_files_in_folder(folder_path):
    count = 0
    for _, _, files in os.walk(folder_path):
        count += len(files)
    return count

def metadata(folder):
    emb = np.zeros((count_files_in_folder(folder), 128))
    for j,m in enumerate(sorted(os.listdir(folder))):
        img=cv2.imread(os.path.join(folder, m))
        emb[j] = embedded_model.embedded(img)
    return emb

def get_existing_json_files(folder_path):
    existing_json_files = set()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                existing_json_files.add(file[:-5])  # Remove '.json' extension
    return existing_json_files

def jsonVectorized(path):
    existing_json_files = get_existing_json_files('data')

    for Id, name in enumerate(sorted(os.listdir(path))):
        if name not in existing_json_files:
            emb = metadata(os.path.join(path, name))
            arr_list = emb.tolist()
            json_string = json.dumps(arr_list)
            create_json_file(name, Id, json_string)

