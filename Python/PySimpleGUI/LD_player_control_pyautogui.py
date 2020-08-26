import autoit
import cv2
import numpy as np
from hidden_capture import capture
import PySimpleGUI as sg

title_temp = 'MANDLOH'
ldp_top_border = 15
hwnd = autoit.win_get_handle(title_temp)
title = autoit.win_get_title_by_handle(hwnd)
print("Title : {}, Hwnd : {}".format(title, hwnd))

ldp_size = autoit.win_get_client_size(title)
layout = [[sg.Graph(ldp_size,(0,ldp_size[1]), (ldp_size[0],0), key='-GRAPH-', enable_events=True, drag_submits=True)],]
window = sg.Window('Demo', layout, location=(10, 10))
a_id = None

while True:
    img = cv2.cvtColor(np.array(capture(hwnd)), cv2.COLOR_RGB2BGR)
    event, values = window.read(timeout=1)
    if event in ('Exit', None):
        break

    elif event == '-GRAPH-': #Mouse down
        mouse_pos = (values['-GRAPH-'][0], values['-GRAPH-'][1])
        autoit.control_click(title, "RenderWindow1", x=int(mouse_pos[0]), y=int(mouse_pos[1]))

    imgbytes = cv2.imencode('.png', img)[1].tobytes()
    if a_id:
        window['-GRAPH-'].delete_figure(a_id)
    a_id = window['-GRAPH-'].draw_image(data=imgbytes, location=(0,0))
    window['-GRAPH-'].TKCanvas.tag_lower(a_id)