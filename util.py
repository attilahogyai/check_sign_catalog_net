import os
from typing import List
import pandas as pd
import numpy as np
from PIL import Image

def list_directory_recursively(directory_path: str) -> List[str] :
    result_files = []
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            file_name = os.path.join(root, name)
            idx = file_name.rindex('/', 0, len(file_name) - len(name) - 1)
            result_files.append(file_name[idx:])
    return result_files

def img_to_df(img_dir: str) -> pd.DataFrame:
    image_list = list_directory_recursively(img_dir)

    df = pd.DataFrame()
    filenames = []
    labels = []
    for file in image_list:
        to = file.find('/', 1)
        label = file[1:to]
        filenames.append(file)
        labels.append(label)
    df['filename'] = filenames
    df['label'] = name_to_idx(labels)
    return df


def name_to_idx(names):
    names_dict = {}
    ordered_names = np.sort(names)
    idx = 0
    for name in ordered_names:
        if None == names_dict.get(name):
            names_dict[name] = idx
            idx = idx+ 1
    return [names_dict.get(name) for name in names]

def get_image(img_root:str, image_path: str, shape: tuple[int,int] = None) -> np.array:
    img = Image.open(img_root + image_path)
    if shape != None:
        img = img.resize(shape)
    img_array = np.array(img)
    img_array = img_array / 255.0
    return img_array