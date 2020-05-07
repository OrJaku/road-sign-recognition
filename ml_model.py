import pandas as pd
import numpy as np
from keras import layers, models, optimizers
from keras.preprocessing.image import ImageDataGenerator

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import os, shutil, cv2

picture_size = 100

numer_of_classes = 3

model = models.Sequential()
model.add(layers.Conv2D(
                    32,
                    (3, 3), 
                    activation='relu', 
                    input_shape=(picture_size, picture_size, 3))
                    )
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.3))

model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(numer_of_classes, activation='softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer="adam",
    metrics=['acc']
    )
model.summary()

model.load_weights('/model_signs.h5')
