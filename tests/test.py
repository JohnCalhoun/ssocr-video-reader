#! /usr/bin/env python3

import time
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
from lib.get_roi import get_roi                                                            
from process import process

Image=cv2.imread("images/raw/373.png")
(W,H,roi,boxes)=get_roi(Image,padding=40)
#border=10
#out=cv2.copyMakeBorder(
#    cv2.resize(cv2.resize(Image,(W,H))[roi[1]:roi[3],roi[0]:roi[2]],(150,80)),
#    border,border,border,border,cv2.BORDER_CONSTANT,None,(0,0,0)
#)
#kernel = np.ones((3,3), np.uint8) 
#out=process(out)
#out = cv2.dilate(out, kernel, iterations=1) 
#out = cv2.erode(out, kernel, iterations=1) 

cv2.imwrite("tmp.png",process(cv2.resize(Image,(W,H))[roi[1]:roi[3],roi[0]:roi[2]]))


