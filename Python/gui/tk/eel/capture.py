import cv2
import eel
import base64
import numpy as np
import autoit
from hidden_capture import capture


hwnd = autoit.win_get_handle("MANDLOH")
title = autoit.win_get_title_by_handle(hwnd)
border_top = 35
scale = 1
eel.init('web')


@eel.expose
def window_capture():
    frame = cv2.cvtColor(np.array(capture(hwnd)), cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, dsize=(0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_b64 = base64.b64encode(jpeg.tobytes())
    jpeg_str = jpeg_b64.decode()
    return jpeg_str


@eel.expose
def mouse_event(x, y):
    print("X: {}, Y: {}".format(int(x/scale), int(y/scale)))
    autoit.control_click(title, "RenderWindow1", x=int(x/scale), y=int((y/scale)-border_top))

eel.start("capture.html")
