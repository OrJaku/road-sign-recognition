from ml_model import ModelInit
from picture_detection import get_picture_detection
from video_detection import get_video_detection

picture_size = 100
number_of_classes = 4
activation_model = "softmax"  # prawdopodobieństwo 1 podzielone na ilość klas
# activation_model = "sigmoid"  # procent prawdopodobieństwa

model_init = ModelInit(picture_size, number_of_classes, activation_model)
model = model_init.model

# Picture detection
get_picture_detection(model, model_init.activation_model, model_init.number_of_classes)

# Video detection
# get_video_detection(model)
