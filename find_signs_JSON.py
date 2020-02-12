import json
import os
import csv

label_of_sign = "information--pedestrians-crossing--g1" #znak przejścia dla pieszych

print("1 - Find one choosen label\n")
print("2 - Get label list \n")
print("0 - Exit program \n")

local_path = os.path.abspath(os.path.dirname(__file__)) #ścieżka lokalna folderu z danymi
external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" #ścieżka sieciowa folderu z danymi
path_to_annotations = os.path.join(external_path, 'annotations') #wybranie folderu z plikami JSON
files_list = os.listdir(path_to_annotations)
i = 1
images = []
label_list = []

respond = input("Chose one: ")

while respond != "0":
    if respond == "1":
        with open('output/image_list.csv', mode="w", newline="") as csv_file:
            i = 1
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
                            file_ = file_[:-5]
                            file_ = file_ + ".jpg"
                            images.append(file_)
                            new_row.writerow([file_])
                            print("FILE", file_)
                            break 
        respond = "0"
        print("Number of images with choosen sign: ", len(images))
        print("CSV file with image name has been save as 'image_list.csv'")
    elif respond == "2":
        with open('output/label_list.csv', mode="w", newline="") as csv_file:
            i = 1
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
                        if label in label_list:
                            pass
                        else:
                            label_list.append(label)
                            new_row.writerow([label])
                            print("New label", label)
        respond = "0"
        print("Number of lables: ", len(label_list))
        print("CSV file with labels has been save as 'label_list.csv'")
    else:
        pass   
print("Exit !")
