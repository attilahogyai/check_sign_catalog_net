import math
import pandas as pd
import config
from util import list_directory_recursively, get_image
import tensorflow as tf
from PIL import Image
import numpy as np

class MyKerasImageGenerator(tf.keras.utils.Sequence):
    def __init__(self, img_root, df, batch_size = 10, image_shape = None, shuffle=True):
        self.img_root = img_root
        self.df = df
        self.train_len = len(df)
        self.batch_size = batch_size
        self.image_shape = image_shape
        self.shuffle = shuffle

    def __data_augmentation(self, img):
        ''' function for apply some data augmentation '''
        img = tf.keras.preprocessing.image.random_shift(img, 0.2, 0.3)
        img = tf.image.random_flip_left_right(img)
        img = tf.image.random_flip_up_down(img)
        return img.image_shape
    def __len__(self):
        return math.ceil(self.train_len / self.batch_size)

    def __on_epoch_end__(self):
        ''' shuffle data after every epoch '''
        # fix on epoch end it's not working, adding shuffle in len for alternative
        pass

    def __getitem__(self, index):
        batch_x = self.df["filename"][index * self.batch_size:(index + 1) * self.batch_size]
        batch_y = self.df["label"][index * self.batch_size:(index + 1) * self.batch_size]
        x = [get_image(self.img_root, file, self.image_shape) for file in batch_x]
        y = batch_y
        return tf.convert_to_tensor(x), tf.convert_to_tensor(y)
