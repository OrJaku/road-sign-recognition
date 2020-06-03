import pandas as pd
import os
from PIL import Image

dataset_path = "/home/kuba-ubuntu/Dokumenty/Datasets"
path_to_train = os.path.join(dataset_path, 'train.p')
path_to_names = os.path.join(dataset_path, 'signnames.csv')

train = pd.read_pickle(path_to_train)
names = pd.read_csv(path_to_names)
dict_signs = names.to_dict()['SignName']
# for i in dict_signs.items():
#     print(i)
x_train, y_train = train['features'], train['labels']
# print(y_train)
#
labels_list_correct = [2, 3, 4, 5, 7, 14, 27]
i = 0
for sign, label in zip(x_train, y_train):
    if label in labels_list_correct:
        i += 1
        img = Image.fromarray(sign, 'RGB')
        sign_name = dict_signs[label]
        sign_name = sign_name.replace(' ', '_')
        sign_name = sign_name.replace('/h)', '')
        sign_name = sign_name.replace('(', '')
        sign_directory = os.path.join("output", sign_name)
        try:
            os.mkdir(sign_directory)
        except FileExistsError:
            pass
        img.save(f'{sign_directory}/{sign_name}_{i}.jpg')

