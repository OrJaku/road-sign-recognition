import numpy as np
import pandas as pd
from keras import layers, models
import matplotlib
import matplotlib.pyplot as plt
import os, cv2
matplotlib.use('TkAgg')

local_path = os.path.abspath(os.path.dirname(__file__))

picture_size = 100
number_of_classes = 4
# activation_model = "softmax"  # prawdopodobieństwo 1 podzielone na ilość klas
activation_model = "sigmoid"  # procent prawdopodobieństwa

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(picture_size, picture_size, 3)))
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

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Dropout(0.25))

model.add(layers.Flatten())
model.add(layers.Dense(1024, activation="relu"))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.25))
model.add(layers.Dense(number_of_classes))
model.add(layers.Activation(activation_model))

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['acc']
)
model.summary()


def load_model(activation):
    return model.load_weights('model_signs_4_multi_classes_{}.h5'.format(activation))


load_model(activation_model)


# ////////////// R-CNN Mask ///////////////
test_dir = os.path.join(local_path, 'picture_test_full')
# figure = plt.figure()
ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
z = 0
print(f'Funkcja aktywacji: {activation_model}')
color = (0, 0, 0)
for e, i in enumerate(os.listdir(test_dir)):
    print(e, i)
    if i.startswith("cross") or i.startswith("stop"):
        plt.figure()
        img = cv2.imread(os.path.join(test_dir, i))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # plt.subplot(3, 4, z+1)
        #
        # plt.tight_layout()
        ss.setBaseImage(img)
        ss.switchToSelectiveSearchFast()
        ssresults = ss.process()
        imout = img.copy()
        probability_list = []
        z += 1
        for w, result in enumerate(ssresults):
            if w < 2000:
                x, y, w, h = result
                timage = imout[y:y+h, x:x+w]
                resized = cv2.resize(timage, (100, 100), interpolation=cv2.INTER_AREA)
                img = np.expand_dims(resized, axis=0)
                out = model.predict(img/255.0, batch_size=10)
                square = w/h
                probability = []
                for class_ in range(number_of_classes):
                    probability_percent = out[0][class_]
                    if class_ != 2:
                        if probability_percent >= 0.75 and 0.88 <= square <= 1.12:
                            probability.append(class_)
                            probability.append(probability_percent)
                            probability.append(result)
                        else:
                            pass
                    else:
                        pass
                if probability:
                    probability_list.append(probability)
                else:
                    pass
        probability_list_array = np.array(probability_list)
        df = pd.DataFrame(data=probability_list_array, columns=["class", "probability", "coordinate"])
        df.sort_values("probability", axis=0, ascending=False, inplace=True, na_position='last')
        max_probability = df.iloc[0]
        class_highest = max_probability[0]
        probability_highest = round(max_probability[1], 3)
        probability_highest = '%.3f' % probability_highest
        coordinate_highest = max_probability[2]
        x, y, w, h = coordinate_highest
        if class_highest == 0:
            class_name = "Przejscie"
            color = (255, 0, 0)
        elif class_highest == 1:
            color = (0, 255, 0)
            class_name = "Ograniczenie 50km/h"
        elif class_highest == 3:
            color = (255, 255, 0)
            class_name = "Stop"
        else:
            class_name = "None"
        print('Max probability {} - Class: {} \n'.format(probability_highest, class_name))
        label = f"{class_name} - {probability_highest}"
        cv2.rectangle(imout, (x, y), (x+w, y+h), color, 1, cv2.LINE_AA)
        cv2.putText(imout, label, (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.2, color, 1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(imout)
        plt.title('{} - {}'.format(probability_highest, class_name, fontsize=3))
    plt.show()
# ///////////////////////////////

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
