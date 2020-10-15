import cv2
import PIL.Image, PIL.ImageTk
from tkinter import *

class App:
    def __init__(self, window):
        self.width, self.height = 640,480
        self.window = window
        self.window.geometry("640x480")
        self.window.title("Tkinter + OpenCV")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.canvas = Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.canvas_on_down = False
        self.tracking = False

        self.delay = 33
        self.update()
        self.window.mainloop()

    def update(self):
        ret, self.frame = self.cap.read()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        if self.canvas_on_down == True:
            self.frame = cv2.rectangle(self.frame, (self.canvas_start_x, self.canvas_start_y), (self.canvas_move_x, self.canvas_move_y), (0, 0, 255), 2)
        
        if self.tracking == True:
            found, track_pos = self.tracker.update(self.frame)
            if found:
                p1 = (int(track_pos[0]), int(track_pos[1]))
                p2 = (int(track_pos[0] + track_pos[2]), int(track_pos[1] + track_pos[3]))
                cv2.rectangle(self.frame, p1, p2, (255,0,0), 2)

        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.window.after(self.delay, self.update)
    
    def mouse_down(self, evt):
        self.canvas_on_down = True
        self.tracking = False
        self.canvas_start_x, self.canvas_start_y = int(evt.x), int(evt.y)
        self.canvas_move_x, self.canvas_move_y = int(evt.x), int(evt.y)

    def mouse_move(self, evt):
        self.canvas_move_x, self.canvas_move_y = int(evt.x), int(evt.y)

    def mouse_up(self, evt):
        self.canvas_on_down = False
        self.tracking = True
        self.tracker = cv2.TrackerCSRT_create()
        bbox = (min(self.canvas_start_x, self.canvas_move_x), min(self.canvas_start_y, self.canvas_move_y), abs(self.canvas_move_x - self.canvas_start_x), abs(self.canvas_move_y - self.canvas_start_y))
        self.tracker.init(self.frame, bbox)

App(Tk())
