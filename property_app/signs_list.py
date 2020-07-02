import json
import os


def signs_list(local_path, json_file_name="signs.json"):
    json_file = os.path.join(local_path,json_file_name)
    with open(json_file, "r") as f:
        steam = json.load(f)
        for n, sign in enumerate(steam):
            print(f'{n+1}. {list(sign.keys())[0]}')
        input("\nWciśniej Enter, aby wrócić do menu...")
