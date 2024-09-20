import os
import shutil
from typing import List
import random
from util import list_directory_recursively

source_path = '/home/attila/work/brickz/insura/images/augmented/'
train_path = '//home/attila/work/brickz/insura/images/train/'
validation_path = '/home/attila/work/brickz/insura/images/validation/'

os.makedirs(train_path, exist_ok=True)
os.makedirs(validation_path, exist_ok=True)



def prepare_dir (target: str) :
    shutil.rmtree(target)
    os.makedirs(target + 'other/', exist_ok=True)
    os.makedirs(target + 'check/', exist_ok=True)
    os.makedirs(target + 'uncheck/', exist_ok=True)


def copy_files(source_dir: str, files_to_move: list[str], target: str) -> None:
    for file in files_to_move:
        src_file_path = source_dir + file
        new_file_path = target + file
        shutil.copy2(src_file_path, new_file_path)


# Example usage
files = list_directory_recursively(source_path)
random.shuffle(files)

train_size = int(len(files) * 0.8)
train_files = files[:train_size]
validation_files = files[train_size:]

prepare_dir(train_path)
copy_files(source_path, train_files, train_path)

prepare_dir(validation_path)
copy_files(source_path, validation_files, validation_path)




