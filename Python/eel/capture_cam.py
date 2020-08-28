import cv2
import eel
import base64
import numpy as np

w, h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #Set caputre size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

eel.init('web')

@eel.expose
def window_capture():
    _, frame = cap.read()
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_b64 = base64.b64encode(jpeg.tobytes())
    jpeg_str = jpeg_b64.decode()
    return jpeg_str


@eel.expose
def mouse_event(x, y):
    print("X: {}, Y: {}".format(x, y))

eel.start("capture.html")
