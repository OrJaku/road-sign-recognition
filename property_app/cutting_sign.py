import os 
import json
import time
from PIL import Image


def cutting_sign(path_to_fully_images, path_to_cut_images, nosign=False, delta_x=2, delta_y=5):

    labels_list = os.listdir(path_to_fully_images)
    time_stamp = time.strftime("%y%m%d%H%M%S")
    for label_of_sign in labels_list:

        path_to_images = os.path.join(path_to_fully_images, label_of_sign)

        if nosign:
            output_cut_path = os.path.join(path_to_cut_images, "nosign")
        else:
            output_cut_path = os.path.join(path_to_cut_images, label_of_sign)
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
                            y_min = round(coordinate["ymin"])
                            y_max = round(coordinate["ymax"])
                            x_min = round(coordinate["xmin"])
                            x_max = round(coordinate["xmax"])
                            width = x_max - x_min
                            height = y_max - y_min
                            # # /// cutting out of the sign ///
                            if nosign:
                                y_min = y_min + (delta_y * height)
                                y_max = y_max + (delta_y * 2 * height)
                                x_min = x_min + (delta_x * width)
                                x_max = x_max + (delta_x * 2 * width)

                            # # /////////
                            area = (x_min, y_min, x_max, y_max)

                            file_jpg = file_ + '.jpg'
                            img = Image.open(os.path.join(path_to_images, file_jpg))

                            img_cut = img.crop(area)
                            print(f'{i} img saved | {width}x{height}')
                            if nosign:
                                img_cut.save(f"{output_cut_path}/nosign_{time_stamp}_{i}.jpg")
                            else:
                                img_cut.save(f"{output_cut_path}/{label_of_sign}_{time_stamp}_{i}.jpg")
    print(f"Directory files: {path_to_cut_images}")
