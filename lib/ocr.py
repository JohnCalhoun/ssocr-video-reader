#! /usr/bin/env python3

import cv2
import numpy as np
from lib.get_roi import get_roi
from lib.process import process
import subprocess
import os
import re
import csv
import logging

def ocr(count,writer,time):
    result = subprocess.run('ssocr -d -1 -c decimal -r 3 images/roi/%s.png'%(count), shell=True,stdout=subprocess.PIPE)
    
    result=str(result.stdout)
    logging.debug("ssocr output: %s"%(result))
    
    value=re.compile("(\d+\.\d\d)").findall(result)[0]
    logging.debug("ssocr output parsed: %s"%(value))
    
    writer.writerow([time,value])


