import os
from find_signs_JSON import find_signs
from chose_image import chose_image

labels_list = [
    "warning--railroad-crossing-with-barriers--g1",
]

local_path = os.path.abspath(os.path.dirname(__file__))  # ścieżka lokalna folderu z danymi

# # Windows
# external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" #ścieżka sieciowa folderu z danymi
# Ubuntu
# external_path = "/run/user/1000/gvfs/smb-share:server=dell-komputer,share=img_mgr/mtsd_fully_annotated"
external_path = "/media/kuba-ubuntu/UUI/test_MGR"
media_usb_path = "/media/kuba-ubuntu/UUI/img_mgr"
while True:
    print("""
    1 - Znajdź wybrane zdjęcia ze znakami lub wygeneruj listę etykiet
    2 - Kopiuj wybrane zdjęcia do nowego katalogu 
    3 - Wytnij znaki z pełnych zdjęć
    4 - Kopiuj wycięte zdjęcia do katalogów (train/valid/test)
    5 - Zmień nazwy plików 
    """)
    resp = input("Chose one: ")
    if resp == "1":
        find_signs(external_path, labels_list)
    elif resp == "2":
        chose_image(local_path, external_path, media_usb_path, labels_list)
    elif resp == "3":
        pass
    else:
        break

# "information--pedestrians-crossing--g1" # znak przejścia dla pieszych
# "regulatory--stop--g1" # znak stop
# "regulatory--stop--g10" # znak stop2
# "regulatory--maximum-speed-limit-50--g1"  #znak ograniczenia predkosco do 50km/h
# "warning--pedestrians-crossing--g5" # znak przejscia dla pieszych ostrzeg.
# "warning--railroad-crossing--g3" # przejazd kolejowy
# "warning--railroad-crossing-with-barriers--g1" # przejazd kolejowy z barierami
