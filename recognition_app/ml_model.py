from keras import models
import matplotlib
import os
matplotlib.use('TkAgg')

local_path = os.path.abspath(os.path.dirname(__file__))
classes = {'cross': 0,
           'limit40': 1,
           'limit50': 2,
           'limit60': 3,
           'limit70': 4,
           'limit80': 5,
           'nosign': 6,
           'othersign': 7,
           'stop': 8,
           'yield': 9,
           }


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
        with open(f'models_json_files/{self.model_structure_file}.json', 'r') as f:
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
