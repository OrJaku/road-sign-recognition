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
    vs = cv2.VideoCapture(file_dir)
    writer = None
    (W, H) = (None, None)

    video_length = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_video_fps = int(vs.get(cv2.CAP_PROP_FPS))
    cap_video_width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_video_height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
    mean = np.array([100, 100, 100], dtype="float32")
    while True:
        (grabbed, frame) = vs.read()
        if not grabbed:
            break
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        output = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (100, 100)).astype("float32")
        frame -= mean

        preds = model.predict(np.expand_dims(frame, axis=0))[0]
        if preds[0] == 0:
            class_name = "Przejscie"
        elif preds[0] == 1:
            class_name = "Ograniczenie 50km/h"
        elif preds[0] == 3:
            class_name = "Stop"
        else:
            class_name = "None"

        text = class_name
        cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 5)
        # check if the video writer is None
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter('out_video.mp4', fourcc, 30,
                                     (W, H), True)
        # write the output frame to disk
        writer.write(output)
        # show the output image
        cv2.imshow("Output", output)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    print("__END__")
