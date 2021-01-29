import cv2
import torch
import numpy as np
from models.experimental import attempt_load
from utils.general import non_max_suppression


with torch.no_grad():
    #source = "5.jpg"
    source = "mb.mp4"
    weights = "mb_best.pt"
    conf_thres = 0.1
    iou_thres = 0.45
    device = "cpu"
    
    model = attempt_load(weights, map_location=device)
    cap = cv2.VideoCapture(source)

    while True:
        ret, img = cap.read()
        img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        out = img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.transpose(2, 0, 1)  #to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes = 0, agnostic=False)
        data = pred[0]
        #print("Found {} items.".format(len(data)))

        for d in data:
            x1, y1, x2, y2, c, l = d
            cv2.rectangle(out, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0),3)
        
        cv2.imshow('out', out)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
