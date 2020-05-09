import pandas as pd
import numpy as np
from keras import layers, models, optimizers
from keras.preprocessing.image import ImageDataGenerator

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os, cv2


picture_size = 100

number_of_classes = 4

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(picture_size, picture_size, 3)))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.2))

model.add(layers.Flatten())
model.add(layers.Dense(1024, activation="relu"))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.25))
model.add(layers.Dense(number_of_classes))
model.add(layers.Activation('softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer="adam",
    metrics=['acc']
)
model.summary()

model.load_weights('model_signs_4_multi_classes.h5')

local_path = os.path.abspath(os.path.dirname(__file__))

# ///////////DISPLAYING IMAGES//////////
# test_dir = os.path.join(local_path, 'test_images')
# figure = plt.figure()
# i = 0
# number_of_test_image = len(test_files)
# for file in test_files:
#
#     path_to_test = os.path.join(test_dir, file)
#     img = cv2.imread(path_to_test)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (picture_size, picture_size))
#     plt.subplot((number_of_test_image // 5) + 2, 5, i+1)
#     plt.tight_layout()
#     plt.xticks([])
#     plt.yticks([])
#     plt.imshow(img)
#     img_tensor = np.reshape(img, [1, picture_size, picture_size, 3])
#     classes = (model.predict_classes(img_tensor)).tolist()
#     correct = ""
#
#     if classes[0] == 0:
#         classes = 'cross'
#
#     elif classes[0] == 2:
#         classes = 'stop'
#
#     elif classes[0] == 1:
#         classes = 'limit50'
#     else:
#         pass
#     if classes != file.split("_")[0]:
#         correct = "Wrong!"
#     plt.title(f"{classes.title()} {correct}", fontsize=6)
#     i += 1
# plt.show()
# //////////////////////////////////////////

# ////////////// R-CNN Mask ///////////////
test_dir = os.path.join(local_path, 'cross_test_full')
figure = plt.figure()
ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
z = 0
for e, i in enumerate(os.listdir(test_dir)):
    print(e, i)
    if i.startswith("cross"):
        img = cv2.imread(os.path.join(test_dir, i))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(3, 3, z+1)
        plt.tight_layout()
        z += 1
        ss.setBaseImage(img)
        ss.switchToSelectiveSearchFast()
        ssresults = ss.process()
        imout = img.copy()
        probably_list = []
        for w, result in enumerate(ssresults):
            if w < 2000:
                x, y, w, h = result
                timage = imout[y:y+h, x:x+w]
                resized = cv2.resize(timage, (100, 100), interpolation=cv2.INTER_AREA)
                img = np.expand_dims(resized, axis=0)
                out = model.predict(img/255.0, batch_size=1)
                square = w/h
                probably_list.append(out[0][0])
                if out[0][0] >= 0.99 and 0.7 <= square <= 1.4:
                    # print(out)
                    cv2.rectangle(imout, (x, y), (x+w, y+h), (0, 255, 0), 1, cv2.LINE_AA)
                    break

        plt.xticks([])
        plt.yticks([])
        plt.imshow(imout)
        print("HP", max(probably_list))
plt.show()
# ///////////////////////////////
