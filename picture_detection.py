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
    color = (0, 0, 0)
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
            probability_list = []
            z += 1
            for w, result in enumerate(ssresults):
                if w < 2000:
                    x, y, w, h = result
                    timage = imout[y:y+h, x:x+w]
                    resized = cv2.resize(timage, (100, 100), interpolation=cv2.INTER_AREA)
                    img = np.expand_dims(resized, axis=0)
                    out = model.predict(img/255.0, batch_size=10)
                    square = w/h
                    probability = []
                    for class_ in range(number_of_classes):
                        probability_percent = out[0][class_]
                        if class_ != 2:
                            if probability_percent >= 0.75 and 0.88 <= square <= 1.12:
                                probability.append(class_)
                                probability.append(probability_percent)
                                probability.append(result)
                            else:
                                pass
                        else:
                            pass
                    if probability:
                        probability_list.append(probability)
                    else:
                        pass
            probability_list_array = np.array(probability_list)
            df = pd.DataFrame(data=probability_list_array, columns=["class", "probability", "coordinate"])
            df.sort_values("probability", axis=0, ascending=False, inplace=True, na_position='last')
            print(df)
            max_probability = df.iloc[0]
            class_highest = max_probability[0]
            probability_highest = round(max_probability[1], 3)
            probability_highest = '%.3f' % probability_highest
            coordinate_highest = max_probability[2]
            x, y, w, h = coordinate_highest
            if class_highest == 0:
                class_name = "Przejscie"
                color = (255, 0, 0)
            elif class_highest == 1:
                color = (0, 255, 0)
                class_name = "Ograniczenie 50km/h"
            elif class_highest == 3:
                color = (255, 255, 0)
                class_name = "Stop"
            else:
                class_name = "None"
            print('Max probability {} - Class: {} \n'.format(probability_highest, class_name))
            label = f"{class_name} - {probability_highest}"
            cv2.rectangle(imout, (x, y), (x+w, y+h), color, 1, cv2.LINE_AA)
            cv2.putText(imout, label, (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.2, color, 1)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(imout)
            plt.title('{} - {}'.format(probability_highest, class_name, fontsize=3))
        plt.show()
