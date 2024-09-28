import create_model
from config import train_dir, validation_dir, checkpoint_path, last_checkpoint_path
from util import img_to_df, get_image, name_to_idx
import numpy as np

model = create_model.create_model()
model.load_weights(last_checkpoint_path)
model.summary()

def calc_results(pred):
    if pred[0] == 1:
        return 0
    elif pred[1] == 1:
        return 1
    else:
        return 2

img_df = img_to_df(validation_dir)

x = np.array([get_image(validation_dir, file, (50,50)) for file in img_df["filename"] ])
predictions = model.predict(x)

result = [calc_results(p) for p in predictions]

img_df["result"]=result
img_df=img_df[img_df["result"] != img_df["label"]]

print(img_df)



#
#
# x = np.array([get_image("/home/hati/stuff/brickz/insura/images/train", file, (50,50)) for file in img_df if file.startswith("/uncheck") ])
# predictions = model.predict(x)
# print(predictions)
#
# x = np.array([get_image("/home/hati/stuff/brickz/insura/images/train", file, (50,50)) for file in img_df if file.startswith("/other") ])
# predictions = model.predict(x)
# print(predictions)
