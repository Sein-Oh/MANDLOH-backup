import cv2, PySimpleGUI as sg

layout = [[sg.Graph((600,450),(0,450), (600,0), key='-GRAPH-', enable_events=True, drag_submits=True)],]
window = sg.Window('Demo', layout, location=(10, 10))
graph_elem = window['-GRAPH-']
a_id = None
mouse_down = False
cap = cv2.VideoCapture(0)
cap.set(3, 320) #Set camera size
cap.set(4, 240)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, dsize=(640, 480), interpolation=cv2.INTER_AREA)
    event, values = window.read(timeout=0)
    if event in ('Exit', None):
        break

    elif event == '-GRAPH-':
        if not mouse_down:
            mouse_start = (values['-GRAPH-'][0], values['-GRAPH-'][1])
        mouse_down = True

    elif event == '-GRAPH-+UP':
        mouse_down = False

    mouse_pos = (values['-GRAPH-'][0], values['-GRAPH-'][1])
    if mouse_down:
        cv2.rectangle(frame, mouse_start, mouse_pos, (0,255,0), 2)
        
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if a_id:
        graph_elem.delete_figure(a_id)
    a_id = graph_elem.draw_image(data=imgbytes, location=(0,0))
    graph_elem.TKCanvas.tag_lower(a_id)
