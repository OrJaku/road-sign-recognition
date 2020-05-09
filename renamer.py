import os
from PIL import Image

path_to_files = os.path.abspath("/home/kuba-ubuntu/img_mgr_out")  # Ubuntu
path_to_out = os.path.abspath("/home/kuba-ubuntu/img_mgr_renamed")  # Ubuntu

try:
    os.mkdir(path_to_out)
except FileExistsError:
    pass

files_list = os.listdir(path_to_files)
i = 3000
for file in files_list:
    i += 1
    img = Image.open(os.path.join(path_to_files, file))
    img.save(f"{path_to_out}/NoSign_{i}.jpg")
    print(f"{i} / {len(files_list)}")
