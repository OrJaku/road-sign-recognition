import os
from ml_model import ModelInit, classes
from picture_detection import get_picture_detection
# from video_detection import get_video_detection

test_picture_folder_name = 'picture_test_full'

local_path = os.path.abspath(os.path.dirname(__file__))
test_picture_direction = os.path.join(local_path, test_picture_folder_name)

model_structure_name = 'model_5conv'
picture_size = 100
number_of_classes = len(classes)
activation_model = "softmax"  # prawdopodobieństwo 1 podzielone na ilość klas
# activation_model = "sigmoid"  # procent prawdopodobieństwa

model_init = ModelInit(picture_size, number_of_classes, activation_model, model_structure_name)
model = model_init.model


# Picture detection
get_picture_detection(model, model_init.activation_model, model_init.number_of_classes, classes, test_picture_direction)

# Video detection
# get_video_detection(model)
