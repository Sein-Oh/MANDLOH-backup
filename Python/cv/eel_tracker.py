import cv2
import eel
import base64
import numpy as np
import webbrowser

cap = cv2.VideoCapture("lsf.mp4")
#w, h = 640, 480
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #set caputre size
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

mouse_pos = [0, 0, 0, 0] #global mouse position x, y, w, h
on_select, on_track = False, False #global mouse status
tracker = None #global tracker
tracker_flag = True #global tracker flag
eel.init('web')

@eel.expose
def capture():
    global on_track, tracker, tracker_flag
    _, frame = cap.read()
    if on_select == True: #draw rectangle
        frame = cv2.rectangle(frame, mouse_pos, (0, 255, 0), 2) #BGR color space
    if on_track == True: #tracking on
        if tracker_flag == True:
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, tuple(mouse_pos))
            tracker_flag = False
        found, track_pos = tracker.update(frame)
        if found:
            p1 = (int(track_pos[0]), int(track_pos[1]))
            p2 = (int(track_pos[0] + track_pos[2]), int(track_pos[1] + track_pos[3]))
            cv2.rectangle(frame, p1, p2, (0,0,255), 2)
        else:
            print("Tracking failed")
            on_track = False
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_b64 = base64.b64encode(jpeg.tobytes())
    jpeg_str = jpeg_b64.decode()
    return jpeg_str

@eel.expose
def mouse_event(type, x0, y0, x1, y1):
    global on_select, on_track, mouse_pos, tracker_flag
    x, y = min(x0, x1), min(y0, y1)
    w, h = abs(max(x0, x1) - x), abs(max(y0, y1) - y)
    mouse_pos = [x, y, w, h]
    if type == "mousedown":
        on_select, on_track = True, False
    if type == "mouseup":
        on_select, on_track, tracker_flag = False, True, True

eel.start("capture.html", mode='edge')