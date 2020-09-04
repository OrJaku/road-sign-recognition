import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import cv2
from .ml_model import classes
import time
matplotlib.use('TkAgg')


def get_picture_detection(model,
                          activation_model,
                          number_of_classes,
                          test_picture_direction,
                          picture_size,
                          save_figure,
                          show_figure,
                          ):
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    z = 0
    print(f'Funkcja aktywacji: {activation_model.upper()} \n')
    loop_time = 0
    for e, i in enumerate(os.listdir(test_picture_direction)):
        b = 0
        print(e, i)
        start_image_recognition = time.time()
        if i.startswith("cross") or \
                i.startswith("stop") or \
                i.startswith("limit") or \
                i.startswith("yield") or \
                i.startswith("no"):
            plt.figure()
            img = cv2.imread(os.path.join(test_picture_direction, i))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height_img, width_img, chanel_img = img.shape
            # Picture resizing
            resized_width_value = 800
            resize_parameter = width_img / resized_width_value
            if resize_parameter <= 1:
                resized_width_value = 600
                resized_height_value = 400
            else:
                resized_height_value = int(height_img / resize_parameter)
            if 0.85 <= height_img/width_img <= 1.2:
                resized_width_value = 600
                resized_height_value = 600
            else:
                pass
            img = cv2.resize(img, (resized_width_value, resized_height_value), interpolation=cv2.INTER_AREA)
            # plt.subplot(3, 4, z+1)
            print(f'Poprzednie (h/w): {height_img}/{width_img}  '
                  f'Nowe (h/w): {resized_height_value}/{resized_width_value} '
                  f'| Parametr zmiany wielkości: {resize_parameter}'
                  )
            ss.setBaseImage(img)
            ss.switchToSelectiveSearchFast()
            ssresults = ss.process()
            imout = img.copy()
            imout_crop = img.copy()
            points_list_cross = []
            points_list_stop = []
            points_list_limit40 = []
            points_list_limit50 = []
            points_list_limit60 = []
            points_list_limit70 = []
            points_list_limit80 = []
            points_list_noovertaking = []
            points_list_yield = []

            z += 1
            for s, result in enumerate(ssresults):
                if s < 2000:
                    x_point, y_point, wight, height = result
                    timage = imout[y_point:y_point + height, x_point:x_point+wight]
                    resized = cv2.resize(timage, (picture_size, picture_size), interpolation=cv2.INTER_AREA)
                    img = np.expand_dims(resized, axis=0)
                    out = model.predict(img/255.0, batch_size=10)
                    square = wight/height
                    found_point = []
                    coordinate_temp = []
                    class_temp = []
                    for class_predicted in range(number_of_classes):
                        probability_percent = out[0][class_predicted]
                        if class_predicted != classes['nosign']:
                            if activation_model == 'softmax':
                                probability_threshold = 0.98
                            elif activation_model == 'sigmoid':
                                probability_threshold = 0.8
                            else:
                                probability_threshold = None
                            if probability_percent >= probability_threshold and 0.88 <= square <= 1.12:
                                found_point.append(class_predicted)
                                found_point.append(probability_percent)
                                found_point.append(result)
                                coordinate_temp.append(result)
                                class_temp.append(class_predicted)
                            else:
                                pass
                        else:
                            pass

                    if found_point:
                        if found_point[0] == classes['cross']:
                            points_list_cross.append(found_point)
                        elif found_point[0] == classes['limit40']:
                            points_list_limit40.append(found_point)
                        elif found_point[0] == classes['limit50']:
                            points_list_limit50.append(found_point)
                        elif found_point[0] == classes['limit60']:
                            points_list_limit60.append(found_point)
                        elif found_point[0] == classes['limit70']:
                            points_list_limit70.append(found_point)
                        elif found_point[0] == classes['limit80']:
                            points_list_limit80.append(found_point)
                        elif found_point[0] == classes['noovertaking']:
                            points_list_noovertaking.append(found_point)
                        elif found_point[0] == classes['stop']:
                            points_list_stop.append(found_point)
                        elif found_point[0] == classes['yield']:
                            points_list_yield.append(found_point)

                    else:
                        pass

            def box_generator(found_points_list):
                frame_thickness = 2
                probability_list_array = np.array(found_points_list)
                df = pd.DataFrame(data=probability_list_array, columns=["klasa", "prawdopodobieństwo", "położenie"])
                df.sort_values("prawdopodobieństwo", axis=0, ascending=False, inplace=True, na_position='last')
                # def get_class_name(classes_dict, class_number):
                #     return [class_name for class_name in classes_dict
                #             if (classes_dict[class_name] == class_number)]
                print(df.iloc[:2])
                max_probability = df.iloc[0]
                probability_highest = round(max_probability[1], 2)
                probability_highest = '%.3f' % probability_highest
                coordinate_highest = max_probability[2]
                x, y, w, h = coordinate_highest
                if found_points_list[0][0] == classes['cross']:
                    class_name = "Przejscie"
                    color_box = (255, 0, 0)
                elif found_points_list[0][0] == classes['limit40']:
                    color_box = (50, 255, 0)
                    class_name = "Ograniczenie 40km/h"
                elif found_points_list[0][0] == classes['limit50']:
                    color_box = (100, 255, 0)
                    class_name = "Ograniczenie 50km/h"
                elif found_points_list[0][0] == classes['limit60']:
                    color_box = (150, 255, 0)
                    class_name = "Ograniczenie 60km/h"
                elif found_points_list[0][0] == classes['limit70']:
                    color_box = (200, 255, 50)
                    class_name = "Ograniczenie 70km/h"
                elif found_points_list[0][0] == classes['limit80']:
                    color_box = (200, 200, 0)
                    class_name = "Ograniczenie 80km/h"
                elif found_points_list[0][0] == classes['noovertaking']:
                    color_box = (0, 100, 255)
                    class_name = "Zakaz wyprzedzania"
                elif found_points_list[0][0] == classes['stop']:
                    color_box = (255, 255, 0)
                    class_name = "Stop"
                elif found_points_list[0][0] == classes['yield']:
                    color_box = (200, 50, 200)
                    class_name = "Ustąp pierwszaństwo"
                else:
                    class_name = "None"
                    color_box = (0, 0, 0)
                probability_highest_percent = float(probability_highest) * 100
                print('Maksymalne prawdopodobieństwo {}% - Klasa: {}'.format(probability_highest_percent, class_name))

                title = f"{class_name}-{probability_highest_percent}%"

                cv2.rectangle(imout, (x, y), (x+w, y+h), color_box, frame_thickness, cv2.LINE_AA)
                delta_box = 8
                sign_preview = imout_crop[y-delta_box:y+h+delta_box, x-delta_box:x+w+delta_box]
                try:
                    sign_preview = cv2.resize(sign_preview,
                                              (int(sign_preview.shape[1]*1.5), int(sign_preview.shape[0]*1.5)))
                except cv2.error:
                    pass
                grid = plt.GridSpec(6, 7,
                                    wspace=0.1,
                                    hspace=0.5,
                                    )
                ax1 = plt.subplot(grid[:5, :5])
                ax1.imshow(imout)
                ax1.axis('off')

                ax2 = plt.subplot(grid[b:1+b, 5:])
                ax2.imshow(sign_preview)
                ax2.set_title(title, fontsize=8)
                ax2.axis('off')
            try:
                box_generator(points_list_cross)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_stop)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_limit40)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_limit50)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_limit60)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_limit70)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_limit80)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_yield)
                b += 1
            except ValueError:
                pass
            try:
                box_generator(points_list_noovertaking)
                b += 1
            except ValueError:
                pass
            if b == 0:
                plt.axis('off')
                plt.imshow(imout)
        if save_figure and show_figure:
            plt.savefig(f'figure_output/figure_{activation_model}_{i}.png')
            plt.show()
            print("Obraz zapisany i wyświetlony\n")
        elif show_figure:
            plt.show()
            print("Obraz wyświetlony\n")
        elif save_figure:
            plt.savefig(f'figure_output/figure_{activation_model}_{i}.png')
            print("Obraz zapisany")
        else:
            pass
        end_image_recognition = time.time()
        recognition_time = end_image_recognition - start_image_recognition
        loop_time = loop_time + int(recognition_time)
        print(f"===== Current loop: {'%.1f' % recognition_time}s == Total time: {'%.1f' %  (loop_time/60)}min =====\n")
    print(f"Total time: {loop_time}sec | {int(loop_time/60)}min")
