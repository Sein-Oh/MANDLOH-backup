import cv2, eel, base64
import numpy as np
import autoit
from window_capture import capture

hwnd = autoit.win_get_handle("web")
eel.init('web')    

@eel.expose
def window_capture():
    frame = cv2.cvtColor(np.array(capture(hwnd)), cv2.COLOR_RGB2BGR)
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_b64 = base64.b64encode(jpeg.tobytes())
    jpeg_str = jpeg_b64.decode()
    return jpeg_str

@eel.expose
def mouse_event(x, y):
    print("X: {}, Y: {}".format(x,y))

eel.start("win_capture.html")
