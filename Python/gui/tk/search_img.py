import cv2
import numpy as np


def search_img(frame, img_path):
    frame = cv2.resize(frame, dsize=(1280, 720), interpolation=cv2.INTER_LINEAR)
    template = cv2.imread(img_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(background,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= 0.7)
    if len(loc[0]) > 0:
        # x = int(np.average(loc[1]))
        # y = int(np.average(loc[0]))
        # cv2.rectangle(img, (x, y, w, h), (0,0,255), 2)
        return True
    else:
        return False