import os
from property_app.find_signs_JSON import find_signs
from property_app.chose_image import chose_image
from property_app.cutting_sign import cutting_sign
from property_app.copy_files import copy_files
from property_app.signs_list import signs_list

labels_list = [
    "regulatory--keep-left--g1",
    "regulatory--keep-right--g2",
    "complementary--keep-right--g1",
    "regulatory--keep-left--g2",
    "regulatory--keep-right--g1",
    "complementary--keep-left--g1",
    "regulatory--yield--g1"
]


local_path = os.path.abspath(os.path.dirname(__file__))  # ścieżka lokalna folderu z danymi
local_path = os.path.join(local_path, "property_app")
# # Windows
# external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" #ścieżka sieciowa folderu z danymi
# Ubuntu
external_path = "/run/user/1000/gvfs/smb-share:server=dell-komputer,share=img_mgr/mtsd_fully_annotated"
# external_path = "/media/kuba-ubuntu/UUI/test_MGR"
output_media_usb_path = "/media/kuba-ubuntu/UUI/img_mgr"
cut_image_out_directory = "/home/kuba-ubuntu/img_mgr_out"
dataset_directory = os.path.abspath("/home/kuba-ubuntu/Pobrane/Data")


while True:
    print("""
    1 - Znajdź wybrane zdjęcia ze znakami lub wygeneruj listę etykiet
    2 - Kopiuj wybrane zdjęcia do nowego katalogu 
    3 - Wytnij znaki z pełnych zdjęć
    4 - Kopiuj wycięte zdjęcia do katalogów (train/valid/test)
    9 - Dostępne znaki
    0 - Koniec
    """)
    resp = input("Wybierz: ")
    if resp == "1":
        find_signs(external_path, labels_list)
    elif resp == "2":
        chose_image(local_path, external_path, output_media_usb_path, labels_list)
    elif resp == "3":
        while True:
            # If nosign -> nosign=True and choose shift parameters delta_x/y
            print("""
            1 - Wybrany znak 
            2 - 'No sign' 
            0 - Powrót 
            """)
            cutting_sign_resp = input("Wybierz: ")
            if cutting_sign_resp == "1":
                cutting_sign(output_media_usb_path, cut_image_out_directory)
            elif cutting_sign_resp == "2":
                delta_resp_x = int(input("Chose delta x parameter: "))
                delta_resp_y = int(input("Chose delta y parameter: "))
                cutting_sign(
                            output_media_usb_path,
                            cut_image_out_directory,
                            nosign=True,
                            delta_x=delta_resp_x,
                            delta_y=delta_resp_y,
                            )
                print(f"Cut 'nosign' with parameters delta x={delta_resp_x}, y={delta_resp_y} ")
            else:
                break
    elif resp == "4":
        copy_files(cut_image_out_directory, dataset_directory)
    elif resp == "9":
        signs_list(local_path)
    else:
        break
