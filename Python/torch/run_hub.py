import cv2
import torch
import numpy as np

model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='mb_best.pt')  # custom model

cap = cv2.VideoCapture('mb.mp4')
while True:
    ret, img = cap.read()
    frame = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = model(img, size=240)
    #convert torch to list
    data = result.xyxy[0].tolist()
    #print('Found {} items.'.format(len(data)))
    if len(data):
        for d in data:
            x1, y1, x2, y2, confidence, label = d
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0), 3)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    cv2.imshow('frame', frame)
    
cv2.destroyAllWindows()
