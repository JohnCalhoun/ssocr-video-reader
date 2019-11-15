#! /usr/bin/env python3

import cv2
import numpy as np
from lib.get_roi import get_roi
from lib.process import process
from lib.ocr import ocr
import subprocess
import os
import re
import csv

def extract(Image,roi,W,H,count,border=10):
    out=cv2.copyMakeBorder(
        cv2.resize(cv2.resize(Image,(W,H))[roi[1]:roi[3],roi[0]:roi[2]],(150,80)),
        border,border,border,border,cv2.BORDER_CONSTANT,None,(0,0,0)
    )
    cv2.imwrite("./images/raw/"+str(count)+".png",Image)  
    cv2.imwrite("./images/roi/"+str(count)+".png",process(out))
    return out


