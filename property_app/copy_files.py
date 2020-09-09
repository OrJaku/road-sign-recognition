import os
import shutil
# path_to_files_input = os.path.abspath("/home/kuba-ubuntu/img_mgr_out")  # Ubuntu
# files_list = os.listdir(path_to_files_input)
# director_output = os.path.abspath("/home/kuba-ubuntu/Pobrane/Data")
# sign = 'nosign'


def coping(origin_path, directory_path, sign_name):
    directories = ["train_data", "valid_data", "test_data"]
    for direction in directories:
        try:
            os.mkdir(os.path.join(directory_path, direction))
        except FileExistsError:
            pass
    dst_train = os.path.join(directory_path, 'train_data', sign_name)
    try:
        os.mkdir(dst_train)
    except FileExistsError:
        pass
    dst_valid = os.path.join(directory_path, 'valid_data', sign_name)
    try:
        os.mkdir(dst_valid)
    except FileExistsError:
        pass
    dst_test = os.path.join(directory_path, 'test_data', sign_name)
    try:
        os.mkdir(dst_test)
    except FileExistsError:
        pass
    origin_path_list = os.listdir(origin_path)
    print("\nOrigin len: {}, Directory: {}".format(len(origin_path_list), origin_path))

    train_files = origin_path_list[0:int(len(origin_path_list)*0.6)]
    print("Train len: ", len(train_files))
    for image_name in train_files:
        src_tr = os.path.join(origin_path, image_name)
        dst_tr = os.path.join(dst_train, image_name)
        shutil.copyfile(src_tr, dst_tr)
    print("train copied")

    valid_files = origin_path_list[int(len(origin_path_list)*0.6):int(len(origin_path_list)*0.9)]
    print("Valid len", len(valid_files))
    for image_name in valid_files:
        src_va = os.path.join(origin_path, image_name)
        dst_va = os.path.join(dst_valid, image_name)
        shutil.copyfile(src_va, dst_va)
    print("validation copied")

    test_files = origin_path_list[int(len(origin_path_list)*0.9):]
    print("Test len :", len(test_files))
    for image_name in test_files:
        src_te = os.path.join(origin_path, image_name)
        dst_te = os.path.join(dst_test, image_name)
        shutil.copyfile(src_te, dst_te)
    print("test copied")


def copy_files(directory_path, director_output):
    files_list = os.listdir(directory_path)
    for directory in files_list:
        directory_path_input = os.path.join(directory_path, directory)
        coping(directory_path_input, director_output, directory)
