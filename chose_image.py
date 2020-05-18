import os
import csv
import shutil

# label_of_sign_1 = "information--pedestrians-crossing--g1" # znak przejścia dla pieszych
# label_of_sign_2 = "regulatory--stop--g1" # znak stop
# label_of_sign_ = "regulatory--stop--g10" # znak stop2
# label_of_sign = "regulatory--maximum-speed-limit-50--g1"  #znak ograniczenia predkosco do 50km/h
# label_of_sign = "warning--pedestrians-crossing--g5" # znak przejscia dla pieszych ostrzeg. 
# label_of_sign = "warning--railroad-crossing--g3" # przejazd kolejowy
# label_of_sign = "warning--railroad-crossing-with-barriers--g1" # przejazd kolejowy z barierami  

labels_list = [
    "regulatory--maximum-speed-limit-60--g1",
    "regulatory--maximum-speed-limit-100--g1",
    "regulatory--maximum-speed-limit-40--g1",
    "regulatory--maximum-speed-limit-70--g1",
    "regulatory--maximum-speed-limit-80--g1",
]


local_path = os.path.abspath(os.path.dirname(__file__))
# external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" # Widnows
external_path = "/run/user/1000/gvfs/smb-share:server=dell-komputer,share=img_mgr/mtsd_fully_annotated" # Ubuntu
media_usb_path = "/media/kuba-ubuntu/UUI/img_mgr"
path_to_images = os.path.join(external_path, 'images')
path_to_labels = os.path.join(external_path, 'annotations')

for label_of_sign in labels_list:
    output_files = os.path.join(local_path, 'output')
    print("Output path", output_files)
    # folder_with_filtered_images = os.path.join(external_path, f'my_image/{label_of_sign}')
    folder_with_filtered_images = os.path.join(media_usb_path, f'{label_of_sign}')

    try:
        os.mkdir(folder_with_filtered_images)
    except FileExistsError:
        print(f"DIr {label_of_sign} exist")
        continue
    files_lable_list = os.listdir(path_to_labels)
    files_list_with_csv = os.listdir(output_files)
    print(files_list_with_csv)
    signs_csv_img_list = []
    i = 1
    j = 1
    k = 1

    with open(f'output/imagelist_label_{label_of_sign}.csv', mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for name in csv_file:
            k += 1
            name_img = name[:-1]
            signs_csv_img_list.append(name_img)
            print(name_img)
            print(f"Converted: {k} files")
        print(signs_csv_img_list)

    for img_name in files_lable_list:
        j += 1
        print(f"Checked: {j} files")
        
        img_name = img_name[:-5]
        img_json_name = img_name + ".json"
        img_jpg_name = img_name + ".jpg"  
        if img_name in signs_csv_img_list:
            i += 1
            shutil.copy(
                    os.path.join(path_to_images, img_jpg_name),
                    folder_with_filtered_images
                    )
            shutil.copy(
                    os.path.join(path_to_labels, img_json_name),
                    folder_with_filtered_images
                    )
            print(f"Copied file {img_name} files {i}")
            signs_csv_img_list.remove(img_name)
    print(f"Copying of {label_of_sign} SUCCESFULL!!")
