import webbrowser
import cv2
import eel
import base64
import numpy as np

host = "localhost"
port = 8000
html = "index.html"
url = "http://{}:{}/{}".format(host, port, html)

mode = 0  # 0: pc / 1: browser / 2: webserver

streaming, tracking = False, False
mouse_on_move, x1, y1, x2, y2 = False, None, None, None, None

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("http://192.168.0.2:8080/video")
ret, frame = cap.read()
tracker = None

eel.init('web')
@eel.expose
def mouse_down(x, y):
    global tracking, x1, y1
    x1, y1 = x, y
    tracking = False


@eel.expose
def mouse_move(x, y):
    global mouse_on_move, x2, y2
    x2, y2 = x, y
    mouse_on_move = True


@eel.expose
def mouse_up():
    global mouse_on_move, tracking, tracker
    tracker = cv2.TrackerKCF_create()
    # tracker = cv2.TrackerTLD_create()
    # tracker = cv2.TrackerMOSSE_create()
    bbox = (x1, y1, x2-x1, y2-y1)
    tracker.init(frame, bbox)
    mouse_on_move = False
    tracking = True


@eel.expose
def toggle_stream():
    global streaming
    streaming = not streaming
    if streaming == True:
        print("Streaming start.")
    else:
        print("Streaming stopped.")


@eel.expose
def setup_cam(width, height):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    eel.setup_img(width, height)


def imshow(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    jpeg_b64 = base64.b64encode(jpeg.tobytes())
    jpeg_str = jpeg_b64.decode()
    eel.js_imshow(jpeg_str)


def loop():
    while True:
        if streaming == True:
            ret, frame = cap.read()
            if mouse_on_move == True:
                frame = cv2.rectangle(
                    frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            if tracking == True:
                ok, bbox = tracker.update(frame)
                if ok:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            imshow(frame)
        eel.sleep(0.001)


eel.spawn(loop)

setup_cam(640, 480)
if mode == 0:
    print("Server is running on desktop")
    eel.start(html, size=(680, 600))

elif mode == 1 or mode == 2:
    if mode == 1:
        webbrowser.open(url)
    print("Server is running on {}".format(url))
    eel.start(html, mode=None, port=port, host=host)
