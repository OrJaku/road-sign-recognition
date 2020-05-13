import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import cv2
matplotlib.use('TkAgg')


def get_video_detection(model):
    local_path = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.join(local_path, 'video_test_full')
    file_dir = os.path.join(test_dir, 'warsaw_drive_cut.mp4')
    print(file_dir)
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    cap = cv2.VideoCapture(file_dir)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_video_fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap_video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(cap_video_fps)
    while True:
        ret, frames = cap.read()
        # video = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
        ss.setBaseImage(frames)
        ss.switchToSelectiveSearchFast()
        ssresults = ss.process()
        for w, result in enumerate(ssresults):
            if w < 2000:
                x, y, w, h = result
                timage = frames[y:y+h, x:x+w]
                resized = cv2.resize(timage, (100, 100), interpolation=cv2.INTER_AREA)
                img = np.expand_dims(resized, axis=0)
                out = model.predict(img/255.0, batch_size=10)
                if out[0][0] == 1:
                    cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 1, cv2.LINE_AA)
        cv2.VideoWriter('output.avi', -1, 20.0, (cap_video_width, cap_video_height))
        # cv2.imshow('video2', frames)
        if cv2.waitKey(33) == 27:
            break
    print("__END__")
