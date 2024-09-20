import os
import random
from typing import Tuple

from PIL import Image, ImageFilter
import numpy as np

from PIL import Image
from PIL.Image import Resampling
import shutil


def get_background_color(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    colors = img.getcolors(maxcolors=1000000)
    most_frequent_color = max(colors, key=lambda x: x[0])
    return most_frequent_color[1]  # Return the RGB value of the most frequent color

def resize_image(image: Image.Image, size: tuple[int,int]) -> Image.Image:
    resized_img = image.resize(size, Resampling.NEAREST)
    return resized_img

def add_noise_to_image(image: Image.Image) -> Image.Image:
    np_image = np.array(image)
    noise = np.random.normal(25, 100, np_image.shape)
    noisy_image = np_image + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

def add_random_rotation(image: Image.Image) -> Image.Image:
    angle = random.uniform(-20, 20)
    return image.rotate(angle, resample=Image.BICUBIC, expand=True)

def add_random_distortion(image: Image.Image) -> Image.Image:
    width, height = image.size
    x_shift = random.randint(-10, 10)
    y_shift = random.randint(-10, 10)
    return image.transform(
        (width, height),
        Image.AFFINE,
        (1, 0, x_shift, 0, 1, y_shift),
        resample=Image.BICUBIC
    )
def zoom_image(image: Image.Image) -> Image.Image:
    zoom_factor = random.randint(7, 13) / 10    # Random zoom between 0.7 and 1.3
    return image.resize((int(image.width * zoom_factor), int(image.height * zoom_factor)), resample=Image.BICUBIC)


def process_images(directory_path: str, output_path: str, nrOfCopies: int) -> None:
    for filename in os.listdir(directory_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory_path, filename)
            image = Image.open(file_path)
            background_color = get_background_color(file_path)
            image = resize_image(image, (50, 50))
            print("Background color (RGB):", background_color)
            for i in range(nrOfCopies):
                zoomed_img = zoom_image(image)
                image = image.convert('RGBA')
                rotated_img = add_random_rotation(image)
                distorted_image = add_random_distortion(rotated_img)
                background_img = Image.new('RGBA', distorted_image.size, background_color)  # white background
                background_img.paste(distorted_image, (0, 0), distorted_image)

                img_to_save = add_noise_to_image(background_img)

                img_to_save_rgb = img_to_save.convert('RGB')
                img_to_save_rgb.save(os.path.join(output_path, f"{i}_noisy_{filename}"))


directory_path = '/home/attila/work/brickz/insura/images/ori/other'
output_path = '/home/attila/work/brickz/insura/images/augmented/other/'
shutil.rmtree(output_path, ignore_errors=True)
os.makedirs(output_path, exist_ok=True)
process_images(directory_path, output_path, 20)

directory_path = '/home/attila/work/brickz/insura/images/ori/check'
output_path = '/home/attila/work/brickz/insura/images/augmented/check/'
shutil.rmtree(output_path, ignore_errors=True)
os.makedirs(output_path, exist_ok=True)
process_images(directory_path, output_path, 50)

directory_path = '/home/attila/work/brickz/insura/images/ori/uncheck'
output_path = '/home/attila/work/brickz/insura/images/augmented/uncheck/'
shutil.rmtree(output_path, ignore_errors=True)
os.makedirs(output_path, exist_ok=True)
process_images(directory_path, output_path, 50)