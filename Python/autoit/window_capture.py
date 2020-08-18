from PIL import ImageGrab
import cv2
import keyboard
import mouse
import numpy as np

def set_roi():
    global ROI_SET, x1, y1, x2, y2
    ROI_SET = False
    print("Select your ROI using mouse drag.")
    while(mouse.is_pressed() == False):
        x1, y1 = mouse.get_position()
        while(mouse.is_pressed() == True):
            x2, y2 = mouse.get_position()
            while(mouse.is_pressed() == False):
                print("Your ROI : {0}, {1}, {2}, {3}".format(x1, y1, x2, y2))
                ROI_SET = True
                return
keyboard.add_hotkey("ctrl+1", lambda: set_roi())
ROI_SET = False
x1, y1, x2, y2 = 0, 0, 0, 0
while True:
    if ROI_SET == True:
        image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
        cv2.imshow("image", image)
        key = cv2.waitKey(10)
        if key == ord("q"):
            print("Quit")
            break
cv2.destroyAllWindows()