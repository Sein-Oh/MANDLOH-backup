import cv2, PySimpleGUI as sg
import tkinter
w, h = 640, 480

layout = [[sg.Graph((w,h),(0,h), (w,0), key='-GRAPH-', enable_events=True, drag_submits=True)],]
window = sg.Window('KCF tracker', layout, location=(10, 10), return_keyboard_events=True)

fig = None
mouse_down = False
tracking = False
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #Set caputre size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

while True:
    ret, frame = cap.read()
    event, values = window.read(timeout=0)
    if event in ('Exit', None):
        break

    elif event == '-GRAPH-': #Mouse down event.
        if not mouse_down: #Triggerd 1 time.
            mouse_start = (values['-GRAPH-'][0], values['-GRAPH-'][1])
        mouse_pos = (values['-GRAPH-'][0], values['-GRAPH-'][1])
        mouse_down = True
        tracking = False

    elif event == '-GRAPH-+UP': #Mouse up event.
        mouse_down = False
        if not tracking:
            tracking = True
            tracker = cv2.TrackerKCF_create()
            bbox = (min(mouse_start[0], mouse_pos[0]), min(mouse_start[1], mouse_pos[1]), abs(mouse_pos[0] - mouse_start[0]), abs(mouse_pos[1] - mouse_start[1]))
            tracker.init(frame, bbox)

    elif event == 'r': #keyboard event
        tracking = False
        print('Release tracking mode.')

    elif event == 'q':
        break

    if mouse_down:
        cv2.rectangle(frame, mouse_start, mouse_pos, (0,255,0), 2)

    if tracking:
        found, track_pos = tracker.update(frame)
        if found:
            p1 = (int(track_pos[0]), int(track_pos[1]))
            p2 = (int(track_pos[0] + track_pos[2]), int(track_pos[1] + track_pos[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2)

    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if fig:
        window['-GRAPH-'].delete_figure(fig)
    fig = window['-GRAPH-'].draw_image(data=imgbytes, location=(0,0))
    window['-GRAPH-'].TKCanvas.tag_lower(fig)
