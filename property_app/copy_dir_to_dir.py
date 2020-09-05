import os
import shutil

path_to_files = "/media/kuba-ubuntu/UUI/img_mgr_2"
destiony_path = "/media/kuba-ubuntu/UUI/img_mgr_3/sign"
path_direction = os.listdir(path_to_files)

for direction in path_direction:
    folder_direction = os.path.join(path_to_files, direction)
    print(folder_direction)
    for image in os.listdir(folder_direction):
        extention = image.split('.')[1]
        if extention == 'jpg':
            src_tr = os.path.join(folder_direction, image)
            print(src_tr)
            dst_tr = os.path.join(destiony_path, image)
            shutil.copyfile(src_tr, dst_tr)
        else:
            pass


# print(path_direction)
# print(" ")
# print(len(path_direction))
