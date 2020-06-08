import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import cv2
matplotlib.use('TkAgg')


def get_picture_detection(model,
                          activation_model,
                          number_of_classes,
                          classes_dict,
                          test_picture_direction,
                          picture_size,
                          save_figure,
                          show_figure,
                          ):
    # figure = plt.figure()
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    z = 0
    print(f'Funkcja aktywacji: {activation_model.upper()}')
    for e, i in enumerate(os.listdir(test_picture_direction)):
        b = 0
        print(e, i)
        if i.startswith("cross") or i.startswith("stop") or i.startswith("limit") or i.startswith("no"):
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
            if 0.9 <= height_img/width_img <= 1.1:
                resized_width_value = 700
                resized_height_value = 700
            else:
                pass
            img = cv2.resize(img, (resized_width_value, resized_height_value), interpolation=cv2.INTER_AREA)
            # plt.subplot(3, 4, z+1)
            print(f'H(o/n): {height_img}/{resized_height_value} x '
                  f'Width(o/n): {width_img}/{resized_width_value} '
                  f'| Resize_parameter: {resize_parameter}'
                  )
            ss.setBaseImage(img)
            ss.switchToSelectiveSearchFast()
            ssresults = ss.process()
            imout = img.copy()
            imout_crop = img.copy()
            classes_list = list(classes_dict)
            points_list_cross = []
            points_list_stop = []
            points_list_limit40 = []
            points_list_limit50 = []
            points_list_limit60 = []
            points_list_limit70 = []
            points_list_limit80 = []
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
                        if class_predicted != 2:
                            if activation_model == 'softmax':
                                probability_threshold = 0.9
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
                        if found_point[0] == 0:
                            points_list_cross.append(found_point)
                        elif found_point[0] == 1:
                            points_list_limit40.append(found_point)
                        elif found_point[0] == 2:
                            points_list_limit50.append(found_point)
                        elif found_point[0] == 3:
                            points_list_limit60.append(found_point)
                        elif found_point[0] == 4:
                            points_list_limit70.append(found_point)
                        elif found_point[0] == 5:
                            points_list_limit80.append(found_point)
                        elif found_point[0] == 7:
                            points_list_stop.append(found_point)
                    else:
                        pass

            def box_generator(found_points_list):
                frame_thickness = 2
                probability_list_array = np.array(found_points_list)
                df = pd.DataFrame(data=probability_list_array, columns=["class", "probability", "coordinate"])
                df.sort_values("probability", axis=0, ascending=False, inplace=True, na_position='last')
                print(df)
                max_probability = df.iloc[0]
                probability_highest = round(max_probability[1], 2)
                probability_highest = '%.3f' % probability_highest
                coordinate_highest = max_probability[2]
                x, y, w, h = coordinate_highest
                if found_points_list[0][0] == 0:
                    class_name = "Przejscie"
                    color_box = (255, 0, 0)
                elif found_points_list[0][0] == 1:
                    color_box = (50, 255, 0)
                    class_name = "Ograniczenie 40km/h"
                elif found_points_list[0][0] == 2:
                    color_box = (100, 255, 0)
                    class_name = "Ograniczenie 50km/h"
                elif found_points_list[0][0] == 3:
                    color_box = (150, 255, 0)
                    class_name = "Ograniczenie 60km/h"
                elif found_points_list[0][0] == 4:
                    color_box = (200, 255, 50)
                    class_name = "Ograniczenie 70km/h"
                elif found_points_list[0][0] == 5:
                    color_box = (200, 200, 0)
                    class_name = "Ograniczenie 80km/h"
                elif found_points_list[0][0] == 7:
                    color_box = (255, 255, 0)
                    class_name = "Stop"
                else:
                    class_name = "None"
                    color_box = (0, 0, 0)
                print('Max probability {} - Class: {} \n'.format(probability_highest, class_name))
                font_scale = 1.2
                font = cv2.FONT_HERSHEY_PLAIN
                title = f"{class_name}-{probability_highest}"
                cv2.putText(imout,
                            class_name,
                            (x, y),
                            font,
                            fontScale=font_scale,
                            color=(255, 255, 255),
                            thickness=frame_thickness
                            )

                cv2.rectangle(imout, (x, y), (x+w, y+h), color_box, 2, cv2.LINE_AA)
                delta_box = 10
                sign_preview = imout_crop[y-delta_box:y+h+delta_box, x-delta_box:x+w+delta_box]
                grid = plt.GridSpec(3, 6,
                                    wspace=0.2,
                                    hspace=0.2,
                                    )
                ax1 = plt.subplot(grid[:3, :3])
                ax1.imshow(imout)
                ax1.axes.xaxis.set_visible(False)
                ax1.axes.yaxis.set_visible(False)

                ax2 = plt.subplot(grid[0+b:1+b, 4])
                ax2.imshow(sign_preview)
                ax2.axes.xaxis.set_visible(False)
                ax2.axes.yaxis.set_visible(False)
                ax2.set_title(title, fontsize=8)
                if b >= 4:
                    ax3 = plt.subplot(grid[-3+b:-3+b, 4])
                    ax3.imshow(sign_preview)
                    ax3.axes.xaxis.set_visible(False)
                    ax3.axes.yaxis.set_visible(False)
                    ax3.set_title(title, fontsize=8)
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
            if b == 0:
                plt.imshow(imout)
        if save_figure and show_figure:
            plt.show()
            plt.savefig(f'figure_output/figure_{activation_model}_{i}.png')
            print("Saved figure")
        elif show_figure:
            plt.show()
        elif save_figure:
            plt.savefig(f'figure_output/figure_{activation_model}_{i}.png')
            print("Saved figure")
        else:
            pass
