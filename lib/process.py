#! /usr/bin/env python3

import numpy as np
import cv2

def process(img):
    kernel = np.ones((5,5), np.uint8) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray,180,255,cv2.THRESH_BINARY)
    image = cv2.bitwise_not(thresh1)
     
    return image


