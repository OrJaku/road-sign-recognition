import os
import argparse
from recognition_app.ml_model import ModelInit, classes
from recognition_app.picture_detection import get_picture_detection

test_picture_folder_name = 'picture_test_full'

local_path = os.path.abspath(os.path.dirname(__file__))
test_picture_direction = os.path.join(local_path, test_picture_folder_name)
model_weight_file = os.path.join(local_path, 'models_weights')
weight_files_list = os.listdir(model_weight_file)

parser = argparse.ArgumentParser()
parser.add_argument("--activ_func", help="Wybierz funkcje aktywacji")
parser.add_argument("--model_file", help="Wybierz plik z modelem")
parser.add_argument("--save", action="store_true")
parser.add_argument("--stopshow", action="store_false")
args = parser.parse_args()
picture_size = 96
number_of_classes = len(classes)
model_structure_name = f'model_{number_of_classes}conv'


if not args.activ_func:
    print("Liczba klas: {}".format(number_of_classes))
    print("1. SOFTMAX (prawdopodobieństwo wystąpienia, podzielone na ilość klas)")
    print("2. SIGMOID (procent prawdopodobieństwa każdej  klasy)")

    while True:
        activation = int(input("Podaj funkcje aktywacji: "))
        if activation == 1:
            activation_model = "softmax"
            break
        elif activation == 2:
            activation_model = "sigmoid"
            break
        else:
            print("Zła funkcja aktywacji")
            activation_model = None
            break
else:
    activation_model = args.activ_func

if not args.model_file:
    i = 1
    weight_files_dict = {}
    for weight_file in weight_files_list:
        weight_file_spaces = weight_file[:-3].split('_')
        for word in weight_file_spaces:
            if word == activation_model:
                weight_files_dict[i] = weight_file
                print(f'{i}. - {weight_file}')
                i += 1
    choose_weight_file = int(input("Wybierz plik [liczba]: "))
    model_weight_file = weight_files_dict[choose_weight_file]
else:
    model_weight_file = args.model_file
model_init = ModelInit(picture_size, number_of_classes, model_weight_file, model_structure_name)
model = model_init.model
print(f"Wyświetlanie zdjęć: {args.stopshow} | Zapis zdjęć: {args.save} \n")
# Picture detection
get_picture_detection(model,
                      activation_model,
                      model_init.number_of_classes,
                      test_picture_direction,
                      picture_size=picture_size,
                      save_figure=args.save,
                      show_figure=args.stopshow
                      )

# Video detection
# get_video_detection(model)
