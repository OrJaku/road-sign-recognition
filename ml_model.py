from keras import models
import matplotlib
import os
matplotlib.use('TkAgg')

local_path = os.path.abspath(os.path.dirname(__file__))
classes = {'cross': 0, 'limit40': 1, 'limit50': 2, 'limit60': 3, 'limit70': 4, 'limit80': 5, 'nosign': 6, 'stop': 7}


class ModelInit:
    def __init__(self, picture_size, number_of_classes, model_weight_file, model_structure_file):
        self.picture_size = picture_size
        self.number_of_classes = number_of_classes
        self.model_weight_file = model_weight_file
        self.model_structure_file = model_structure_file
        self._model = None

    @property
    def model(self):
        if not self._model:
            self._model = self.load_model()
        return self._model

    def get_model(self):
        with open(f'models_json_files/{self.model_structure_file}_2.json', 'r') as f:
            model = models.model_from_json(f.read())
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
        model.load_weights('models_weights/{0}'.format(self.model_weight_file))
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
