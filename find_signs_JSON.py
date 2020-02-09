import json
import os
import csv

label_of_sign = "information--pedestrians-crossing--g1" #znak przejścia dla pieszych

local_path = os.path.abspath(os.path.dirname(__file__)) #ścieżka lokalna folderu z danymi
external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" #ścieżka sieciowa folderu z danymi
path_to_annotations = os.path.join(external_path, 'annotations') #wybranie folderu z plikami JSON
files_list = os.listdir(path_to_annotations)
len(files_list)
images = []
i = 1
with open('output/image_list.csv', mode="w") as csv_file:
    new_row = csv.writer(
        csv_file, 
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
        )
    for file_ in files_list:
        i += 1
        json_file = os.path.join(path_to_annotations, file_)
        print(f"{i} / {len(files_list)}")
        with open(json_file, "r") as f:
            steam = json.load(f)
            objects = steam['objects']
            for properties in objects:
                label = properties["label"]
                if label == label_of_sign and file_ not in images:
                    print("FILE", file_) 
                    images.append(file_)
                    new_row.writerow([file_])
                 
print(images)
print("Number of images with choosen sign: ", len(images))
print("CSV file with image name has been save as 'image_list.csv'")
