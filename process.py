#! /usr/bin/env python3

import time
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2

def process(img):
    kernel = np.ones((5,5), np.uint8) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray,180,255,cv2.THRESH_BINARY)
    erode = cv2.dilate(thresh1, kernel, iterations=1) 
    #dilate = cv2.erode(erode, kernel, iterations=1) 
    image = cv2.bitwise_not(thresh1)
     
    return image
#cv2.imshow('Original Image', dilate) 
#cv2.waitKey(0)


