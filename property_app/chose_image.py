import os
import shutil


def chose_image(
                local_path_of_app,
                path_to_fully_images,
                copy_chose_image_directory,
                labels_chose,
                load_json_file_directory="annotations",
                load_jpeg_file_directory="images",
                csv_with_labels_directory="output",
                ):
    path_to_images = os.path.join(path_to_fully_images, load_jpeg_file_directory)
    path_to_labels = os.path.join(path_to_fully_images, load_json_file_directory)

    for label_of_sign in labels_chose:
        output_files = os.path.join(local_path_of_app, csv_with_labels_directory)
        print("Output path", output_files)
        folder_with_filtered_images = os.path.join(copy_chose_image_directory, f'{label_of_sign}')
        try:
            os.mkdir(folder_with_filtered_images)

        except FileExistsError:
            while True:
                print(f"Dir {label_of_sign} exist")
                existing_directory_check = input(f"Czy usunąć folder {label_of_sign} i stworzyć nowy ? [y/n]")
                if existing_directory_check == 'y':
                    shutil. rmtree(folder_with_filtered_images)
                    os.mkdir(folder_with_filtered_images)
                    break
                elif existing_directory_check == 'n':
                    break
                else:
                    pass
        files_lable_list = os.listdir(path_to_labels)
        files_list_with_csv = os.listdir(output_files)
        print(files_list_with_csv)
        signs_csv_img_list = []
        i = 1
        j = 1
        k = 1
        with open(f'property_app/output/imagelist_label_{label_of_sign}.csv', mode="r") as csv_file:
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
                print(f"Copied file '{img_name}' || Found {i} files ")
                signs_csv_img_list.remove(img_name)
        print(f"Directory files: {copy_chose_image_directory}")
        print(f"Copied signs: '{label_of_sign}'\n Done!")
