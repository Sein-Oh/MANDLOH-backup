import cv2
import eel
import base64
import numpy as np

cap = cv2.VideoCapture(0)
w, h = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)  # set caputre size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

mouse_pos = [0, 0, 0, 0]  # global mouse position
bbox = None
on_select, on_track = False, False  # global mouse status
tracker = None  # global tracker
tracker_flag = True  # global tracker flag
eel.init('web')


@eel.expose
def capture():
    global on_track, tracker, tracker_flag
    _, frame = cap.read()
    if on_select == True:  # draw rectangle
        frame = cv2.rectangle(frame, bbox, (0, 255, 0), 2)  # BGR color space
    if on_track == True:  # tracking on
        if tracker_flag == True:
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, bbox)
            tracker_flag = False
        found, track_pos = tracker.update(frame)
        if found:
            p1 = (int(track_pos[0]), int(track_pos[1]))
            p2 = (int(track_pos[0] + track_pos[2]),
                  int(track_pos[1] + track_pos[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255), 2)
        else:
            print("Tracking failed")
            on_track = False
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_b64 = base64.b64encode(jpeg.tobytes())
    jpeg_str = jpeg_b64.decode()
    return jpeg_str


@eel.expose
def mouse_event(type, x, y):
    global on_select, on_track, tracker_flag, mouse_pos, bbox
    if type == "start":
        on_select, on_track = True, False
        mouse_pos[:2] = x, y

    elif type == "move":
        mouse_pos[2:] = x, y

    w, h = abs(mouse_pos[0] - mouse_pos[2]), abs(mouse_pos[1] - mouse_pos[3])
    bbox = (min(mouse_pos[0], mouse_pos[2]),
            min(mouse_pos[1], mouse_pos[3]), w, h)

    if type == "end":
        if min(bbox[2:]) < 5:
            on_select, on_track, tracker_flag = False, False, False
            print("Boundary box too small. Select again.")
        else:
            on_select, on_track, tracker_flag = False, True, True


eel.start("capture.html")
