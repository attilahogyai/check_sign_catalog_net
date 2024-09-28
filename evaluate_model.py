import create_model
from config import train_dir, validation_dir, checkpoint_path, last_checkpoint_path
from util import img_to_df, get_image, name_to_idx
import numpy as np

model = create_model.create_model()
model.load_weights(last_checkpoint_path)
model.summary()

img_df = img_to_df(validation_dir)

#x = [get_image(validation_dir, file, (50,50)) for file in img_df["filename"]]
#y = [label for label in img_df["label"]]


x = np.array([get_image("/home/hati/stuff/brickz/insura/images/train", "/check/47_noisy_proxy-image (58).jpeg", (50,50))])
labels = np.array([1])
y = labels
loss, acc = model.evaluate(x, y, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
