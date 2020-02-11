import os
import csv
import shutil

local_path = os.path.abspath(os.path.dirname(__file__))
external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" 
path_to_images = os.path.join(external_path, 'images')
folder_with_filtered_images = os.path.join(external_path, 'filtered_img')
files_list = os.listdir(path_to_images)
signs_csv_list = []
i = 1
j = 1
k = 1
with open('output/image_list.csv', mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for name in csv_file:
        k += 1
        name = name[:-1]
        signs_csv_list.append(name)
        print(name)
        print(f"Converted: {k} files")
    print(signs_csv_list)

for img_name in files_list:
    j += 1
    print(f"Checked: {j} files")
    if img_name in signs_csv_list:
        i += 1
        new_path = shutil.copy(
            os.path.join(
                path_to_images, img_name), 
                folder_with_filtered_images
                )
        print(f"Copied file {img_name} files {i}")
        signs_csv_list.remove(img_name)
print("COPYING SUCCESFULL !!")
