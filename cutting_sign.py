import os 
import json
from PIL import Image

# znak przejścia dla pieszych
# label_of_sign = "information--pedestrians-crossing--g1"
# znak stop
# label_of_sign = "regulatory--stop--g1"
# znak stop2
# label_of_sign = "regulatory--stop--g10"


path_to_files = os.path.abspath("E:/img_mgr")
labels_list = os.listdir(path_to_files)
# path_to_files = os.path.abspath("C:/Users/Jakub/Desktop/picture")
path_to_out = os.path.abspath("C:/Users/Jakub/Desktop/picture/out")
for label_of_sign in labels_list:
    path_to_images = os.path.join(path_to_files, label_of_sign)
    output_cut_path = os.path.join(path_to_out, label_of_sign)
    try:
        os.mkdir(output_cut_path)
    except FileExistsError:
        pass

    files_list = os.listdir(path_to_images)
    i = 0
    for file_name in files_list:
        
        file_split = file_name.split('.')
        extantion = file_split[1]
        file_ = file_split[0]
        if extantion == "json":
            json_file = os.path.join(path_to_images, file_name)
            with open(json_file, "r") as f:
                steam = json.load(f)
                objects = steam["objects"]
                for properties in objects:
                    label = properties["label"]
                    if label == label_of_sign:       
                        i += 1
                        coordinate = properties["bbox"]
                        extetend_value = 10
                        y_min = round(coordinate["ymin"])
                        y_max = round(coordinate["ymax"]) 
                        x_min = round(coordinate["xmin"]) 
                        x_max = round(coordinate["xmax"])
                        width = x_max - x_min
                        height = y_max - y_min
                        area = (x_min, y_min, x_max, y_max)

                        file_jpg = file_ + '.jpg'
                        img = Image.open(os.path.join(path_to_images, file_jpg))

                        img_cut = img.crop(area)
                        output_cut_path
                        print(f'{i} img saved')
                        img_cut.save(f"{output_cut_path}/{label_of_sign}_{i}.jpg")
