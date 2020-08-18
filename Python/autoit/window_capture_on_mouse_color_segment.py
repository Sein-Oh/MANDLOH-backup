import autoit
import cv2
import numpy as np
import PIL
from PIL import ImageGrab

w, h = 80, 100
win_title = 'MANDLOH'
win_pos = autoit.win_get_pos(win_title)  # 앱플레이어 위치
cv2.namedWindow(win_title)
cv2.namedWindow('red')
cv2.namedWindow('green')
cv2.namedWindow('blue')
cv2.moveWindow(win_title, win_pos[0]+win_pos[2], 0)
cv2.moveWindow('red', win_pos[0]+win_pos[2], (h+30) * 1)
cv2.moveWindow('green', win_pos[0]+win_pos[2], (h+30) * 2)
cv2.moveWindow('blue', win_pos[0]+win_pos[2], (h+30) * 3)

#색상 분리
lower_blue = np.array([110, 100, 100])
upper_blue = np.array([130, 255, 255])
lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
lower_red = np.array([-10, 100, 100])
upper_red = np.array([10, 255, 255])

while True:
    x, y = autoit.mouse_get_pos()
    x1, y1 = int((x - w/2)), int(y - h)
    x2, y2 = int((x + w/2)), y
    cropped_img = cv2.cvtColor(
        np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)

    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    blue_range = cv2.inRange(hsv, lower_blue, upper_blue)
    green_range = cv2.inRange(hsv, lower_green, upper_green)
    red_range = cv2.inRange(hsv, lower_red, upper_red)
    blue_result = cv2.bitwise_and(cropped_img, cropped_img, mask=blue_range)
    red_result = cv2.bitwise_and(cropped_img, cropped_img, mask=red_range)
    green_result = cv2.bitwise_and(cropped_img, cropped_img, mask=green_range)

    cv2.imshow(win_title, cropped_img)
    cv2.imshow('blue', blue_result)
    cv2.imshow('red', red_result)
    cv2.imshow('green', green_result)
    key = cv2.waitKey(1)
    if key == ord('q'):
        print('Quit')
        break
cv2.destroyAllWindows()
