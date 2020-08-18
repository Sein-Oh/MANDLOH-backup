import autoit
import cv2
import numpy as np
import PIL
from PIL import ImageGrab

win_cap = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)
cv2.namedWindow('capture', cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow('capture', 1300, 0)
cv2.setWindowProperty('capture', cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)
roi = cv2.selectROI('capture', win_cap, False)
cv2.destroyWindow('capture')

x1, y1, x2, y2 = roi[0], roi[1], roi[2]+roi[0], roi[3]+roi[1]
while True:
    cropped_img = cv2.cvtColor(
        np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
    cv2.imshow('img', cropped_img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        print("Quit")
        break
cv2.destroyAllWindows()