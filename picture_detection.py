import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import cv2
matplotlib.use('TkAgg')


def get_picture_detection(model, activation_model, number_of_classes):
    local_path = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.join(local_path, 'picture_test_full')
    # figure = plt.figure()
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    z = 0
    print(f'Funkcja aktywacji: {activation_model}')
    for e, i in enumerate(os.listdir(test_dir)):
        print(e, i)
        if i.startswith("cross") or i.startswith("stop"):
            plt.figure()
            img = cv2.imread(os.path.join(test_dir, i))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # plt.subplot(3, 4, z+1)
            # plt.tight_layout()
            ss.setBaseImage(img)
            ss.switchToSelectiveSearchFast()
            ssresults = ss.process()
            imout = img.copy()
            found_points_list_cross = []
            found_points_list_stop = []
            found_points_list_limit50 = []
            z += 1
            for s, result in enumerate(ssresults):
                if s < 2000:
                    x_point, y_point, wight, height = result
                    timage = imout[y_point:y_point + height, x_point:x_point+wight]
                    resized = cv2.resize(timage, (100, 100), interpolation=cv2.INTER_AREA)
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
                            found_points_list_cross.append(found_point)
                        elif found_point[0] == 1:
                            found_points_list_limit50.append(found_point)
                        elif found_point[0] == 3:
                            found_points_list_stop.append(found_point)

                    else:
                        pass

            def box_generator(found_points_list):
                probability_list_array = np.array(found_points_list)
                df = pd.DataFrame(data=probability_list_array, columns=["class", "probability", "coordinate"])
                df.sort_values("probability", axis=0, ascending=False, inplace=True, na_position='last')
                print(df)
                max_probability = df.iloc[0]
                class_highest = max_probability[0]
                probability_highest = round(max_probability[1], 3)
                probability_highest = '%.3f' % probability_highest
                coordinate_highest = max_probability[2]
                x, y, w, h = coordinate_highest
                if found_points_list[0][0] == 0:
                    class_name = "Przejscie"
                    color_box = (255, 0, 0)
                elif found_points_list[0][0] == 1:
                    color_box = (0, 255, 0)
                    class_name = "Ograniczenie 50km/h"
                elif found_points_list[0][0] == 3:
                    color_box = (255, 255, 0)
                    class_name = "Stop"
                else:
                    class_name = "None"
                    color_box = (0, 0, 0)
                print('Max probability {} - Class: {} \n'.format(probability_highest, class_name))
                font_scale = 0.8
                font = cv2.FONT_HERSHEY_PLAIN

                rectangle_bgr = (255, 255, 255)

                text = f"{class_name} - {probability_highest}"

                (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]

                text_offset_x = 10
                text_offset_y = imout.shape[0] - 25

                box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
                # cv2.rectangle(imout, (x, y), (x+10, y+10), rectangle_bgr, cv2.FILLED)
                cv2.putText(imout, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0, 0, 0), thickness=1)

                cv2.rectangle(imout, (x, y), (x+w, y+h), color_box, 1, cv2.LINE_AA)
            try:
                box_generator(found_points_list_cross)
            except ValueError:
                pass
            try:
                box_generator(found_points_list_limit50)
            except ValueError:
                pass
            try:
                box_generator(found_points_list_stop)
            except ValueError:
                pass
            plt.xticks([])
            plt.yticks([])
            plt.imshow(imout)
            # plt.title('{} - {}'.format(probability_highest, class_name, fontsize=3))
        plt.show()

