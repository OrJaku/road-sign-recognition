from keras import layers, models
import matplotlib
import os
matplotlib.use('TkAgg')

local_path = os.path.abspath(os.path.dirname(__file__))


class ModelInit:
    def __init__(self, picture_size, number_of_classes, activation_model):
        self.picture_size = picture_size
        self.number_of_classes = number_of_classes
        self.activation_model = activation_model
        self._model = None

    @property
    def model(self):
        if not self._model:
            self._model = self.load_model()
        return self._model

    def get_model(self):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.picture_size, self.picture_size, 3)))
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
        model.add(layers.Dense(self.number_of_classes, activation=self.activation_model))

        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['acc']
        )
        # model.summary()
        print("Model loaded")
        return model

    def load_model(self):
        print("Weights loaded")
        model = self.get_model()
        model.load_weights('model_signs_4_multi_classes_{}.h5'.format(self.activation_model))
        return model

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
