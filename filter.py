import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter


local = os.path.abspath(os.path.dirname(__file__))

file = "yield_2.jpg"
test_picture_folder = 'picture_test_full_t'


def picture_filter(local_path, test_picture_folder_name, file_name):
    plt.figure()
    boundaries = [
        ([128, 0, 0], [255, 160, 128]),
        ([86, 31, 4], [220, 88, 50]),
        ([25, 146, 190], [62, 174, 250]),
        ([103, 86, 65], [145, 133, 128]),
    ]

    test_picture_direction = os.path.join(local_path, test_picture_folder_name)
    img = cv2.imread(os.path.join(test_picture_direction, file_name))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # img = Image.open(os.path.join(test_picture_direction, file_name))
    # kernel = np.array([[-1,-1,-1],
    #                    [-1, 9,-1],
    #                    [-1,-1,-1]])
    # img = cv2.filter2D(img, -1, kernel)
    plt.imshow(img)
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        # show the images
        cv2.imshow("images", np.hstack([img, output]))
        # plt.show()
        cv2.waitKey(0)
    # img.show()
    # sharpened1 = img.filter(ImageFilter.SHARPEN)
    # sharpened1.show()


picture_filter(local, test_picture_folder, file)
