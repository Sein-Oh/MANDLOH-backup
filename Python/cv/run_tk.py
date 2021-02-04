import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
from tkinter import *

class App:
    def __init__(self, window):
        self.width, self.height = 416, 416
        self.size = 416 #image size for yolo
        self.window = window
        self.window.geometry("600x600")
        self.window.title("Tkinter + OpenCV")
        self.cap = cv2.VideoCapture("mb.mp4")
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.canvas = Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.canvas_on_down = False
        self.canvas_start_x, self.canvas_start_y = None, None
        self.canvas_move_x, self.canvas_move_y = None, None

        self.CONF_THRESH, self.NMS_THRESH = 0.5, 0.5
        self.net = cv2.dnn.readNetFromDarknet("custom-yolov4-tiny-detector.cfg", "custom-yolov4-tiny-detector_best.weights")
        self.output_layers = [self.net.getLayerNames()[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.delay = 1
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, dsize=(self.size, self.size), interpolation=cv2.INTER_AREA)
        
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.output_layers)
        class_ids, confidences, b_boxes = [], [], []
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > self.CONF_THRESH:
                    center_x, center_y, w, h = (detection[0:4] * np.array([self.size, self.size, self.size, self.size])).astype('int')
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    b_boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        with open("obj.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]

        if len(b_boxes) > 0:
            indices = cv2.dnn.NMSBoxes(b_boxes, confidences, self.CONF_THRESH, self.NMS_THRESH).flatten().tolist()
            for index in indices:
                x, y, w, h = b_boxes[index]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 2)
                cv2.putText(frame, classes[class_ids[index]], (x + 5, y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)

        if self.canvas_on_down == True:
            frame = cv2.rectangle(frame, (self.canvas_start_x, self.canvas_start_y), (self.canvas_move_x, self.canvas_move_y), (0, 0, 255), 2)
        
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.window.after(self.delay, self.update)
    
    def mouse_down(self, evt):
        self.canvas_on_down = True
        self.canvas_start_x, self.canvas_start_y = int(evt.x), int(evt.y)
        self.canvas_move_x, self.canvas_move_y = int(evt.x), int(evt.y)

    def mouse_move(self, evt):
        self.canvas_move_x, self.canvas_move_y = int(evt.x), int(evt.y)

    def mouse_up(self, evt):
        self.canvas_on_down = False

App(Tk())