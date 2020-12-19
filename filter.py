import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter


local = os.path.abspath(os.path.dirname(__file__))

file = "yield_2.jpg"
file = "cross_6.jpeg"
file = "stop_12.jpeg"
file = "limit40_2.jpg"

test_picture_folder = 'picture_test_full_t'



def picture_filter(local_path, test_picture_folder_name, file_name):
    plt.figure()
    # yellow
    # blue
    # red
    # white
    boundaries = [
        (np.array([0, 128, 130]), np.array([32, 255, 255])),
        (np.array([96, 120, 0]), np.array([150, 255, 255])),
        (np.array([133, 88, 0]), np.array([179, 255, 255])),

    ]
    test_picture_direction = os.path.join(local_path, test_picture_folder_name)
    img = cv2.imread(os.path.join(test_picture_direction, file_name))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # img = Image.open(os.path.join(test_picture_direction, file_name))
    # kernel = np.array([[-1,-1,-1],
    #                    [-1, 9,-1],
    #                    [-1,-1,-1]])
    # img = cv2.filter2D(img, -1, kernel)
    # plt.imshow(img)
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries

        mask = cv2.inRange(img_hsv, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        # show the images
        cv2.imshow("images", np.hstack([img, output]))
        # plt.show()
        cv2.waitKey(0)
    # img.show()
    # sharpened1 = img.filter(ImageFilter.SHARPEN)
    # sharpened1.show()


picture_filter(local, test_picture_folder, file)
