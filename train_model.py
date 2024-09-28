import tensorflow as tf
from keras.src.layers import Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import create_model
from config import train_dir, validation_dir, checkpoint_path, last_checkpoint_path
from MyKerasImageGenerator import MyKerasImageGenerator
from util import img_to_df
from tensorflow.keras.callbacks import TensorBoard

# Define directory paths

# Create ImageDataGenerator instances
train_img = img_to_df(train_dir)

train_datagen = MyKerasImageGenerator(
    train_dir,
    train_img,
    image_shape=(50, 50)
)
validation_img = img_to_df(validation_dir)
validation_datagen = MyKerasImageGenerator(
    validation_dir,
    validation_img,
    image_shape=(50, 50)
)
#validation_datagen = ImageDataGenerator(rescale=1./255)

# Load images from directories
# train_generator = train_datagen.flow_from_directory(
#    train_dir,
#    target_size=(50, 50),
#    batch_size=32,
#    class_mode='binary'
#)

#validation_generator = validation_datagen.flow_from_directory(
#    validation_dir,
#    target_size=(50, 50),
#    batch_size=32,
#    class_mode='binary'
#)

# TensorBoard(log_dir="./log",
#                          histogram_freq=1,
#                          write_graph=True,
#                          write_images=True,
#                          update_freq='epoch',
#                          profile_batch=2,
#                          embeddings_freq=1)

cp_callback = [tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    verbose=1,
    save_weights_only=True)] # *n_batches

# Define a simple model
model = create_model.create_model()

# Train the model
model.fit(
    train_datagen,
    steps_per_epoch=100,
    epochs=100,
    validation_data=validation_datagen,
    validation_steps=50,
    verbose=1,
    callbacks=[cp_callback]
)
model.save_weights(last_checkpoint_path)