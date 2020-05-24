import os
from find_signs_JSON import find_signs

local_path = os.path.abspath(os.path.dirname(__file__))  # ścieżka lokalna folderu z danymi

# # Windows
# external_path = "\\\\Dell-komputer\img_mgr\mtsd_fully_annotated" #ścieżka sieciowa folderu z danymi
# Ubuntu
external_path = "/run/user/1000/gvfs/smb-share:server=dell-komputer,share=img_mgr/mtsd_fully_annotated"

labels_list = [
                "regulatory--maximum-speed-limit-80--g1",
                 ]

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
        pass
    else:
        pass