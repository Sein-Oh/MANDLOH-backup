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
        self.canvas.bind("<Key>", self.key_down)
        self.canvas.focus_set() # For <Key> event
        self.canvas_on_down = False
        self.canvas_start_x, self.canvas_start_y = None, None
        self.canvas_move_x, self.canvas_move_y = None, None

        self.delay = 33
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Change the color space to RGB
        if self.canvas_on_down == True:
            frame = cv2.circle(frame, (self.canvas_start_x, self.canvas_start_y), 35, (131, 245, 239), 3)
            frame = cv2.circle(frame, (self.canvas_move_x, self.canvas_move_y), 30, (244, 89, 163), -1)
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
    
    def key_down(self, evt):
        print(evt.char)

App(Tk())