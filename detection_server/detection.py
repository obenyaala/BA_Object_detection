# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:11:05 2020

@author: WN00151959
"""

import cv2,os
import time

FOLDER = "Models/graph_inception_coco"
WRITE = "D:/Desktop/BA/savedFTPImages"
FROZEN_GRAPH_PATH = os.path.join(FOLDER,"frozen_inference_graph.pb")
LABEL_MAP_PATH = os.path.join(FOLDER, "lbl.pbtxt")

cvNet = cv2.dnn.readNetFromTensorflow(FROZEN_GRAPH_PATH, LABEL_MAP_PATH)

def get_detection(path):
    tic = time.perf_counter()
    time.sleep(0.4)
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    time.sleep(0.4)
    img = cv2.resize(img, (409,300))
    cvNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 409), swapRB=True, crop=False))
    cvOut = cvNet.forward()
    time.sleep(0.1)
    rows = img.shape[0]
    cols = img.shape[1]
    
    best = 0
    res = (-1,-1)
    for detection in cvOut[0,0,:,:]:
        score = float(detection[2])
        if score > 0.3:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            circle = (int(left+(right-left)/2),int(top+(bottom-top)/2))
            if score > best:
                best = score
                res = circle
    if res != (-1,-1): 
        print("this is detected point:",res)
        cv2.circle(img,res, 8, (0,0,255), -1)
        time.sleep(0.1)
        toc = time.perf_counter()
        print(f"Erkennung in {toc - tic:0.4f} seconds")
    
    cv2.imwrite(WRITE+"\image.jpg",img)
    os.remove(path)        
    
    return res
    

    