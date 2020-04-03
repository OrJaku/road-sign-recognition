import os
import csv
import shutil

local_path = os.path.abspath(os.path.dirname(__file__))
external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" 
path_to_images = os.path.join(external_path, 'images')
output_files = os.path.join(local_path, 'output')
print("Output path", output_files)
folder_with_filtered_images = os.path.join(external_path, 'my_image/regulatory--stop--g10')
files_list = os.listdir(path_to_images)
files_list_with_csv = os.listdir(output_files)
print(files_list_with_csv)
signs_csv_list = []
i = 1
j = 1
k = 1

# for i in 
# respond = input("Chose one: ")

# while respond != "0":
#     if respond == i
with open(f'output/imagelist_regulatory--stop--g10.csv', mode="r") as csv_file:
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
