#! /usr/bin/env python3

import cv2
import numpy as np
from lib.get_roi import get_roi
import subprocess
import os
from process import process
import re
import csv

vidcap = cv2.VideoCapture('data/scale-readings-2.mp4')
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
count=0
frameRate=vidcap.get(cv2.CAP_PROP_FPS)
hasFrames,Image=vidcap.read()

def extract(Image,roi,W,H,count,border=10):
    out=cv2.copyMakeBorder(
        cv2.resize(cv2.resize(Image,(W,H))[roi[1]:roi[3],roi[0]:roi[2]],(150,80)),
        border,border,border,border,cv2.BORDER_CONSTANT,None,(0,0,0)
    )
    cv2.imwrite("./images/raw/"+str(count)+".png",Image)  
    cv2.imwrite("./images/roi/"+str(count)+".png",process(out))
    return out

def ocr(count,writer,time):
    result = subprocess.run('%s/ssocr -d -1 -c decimal -r 3 images/roi/%s.png'%(__location__,count), shell=True,stdout=subprocess.PIPE)
    result=str(result.stdout)
    value=re.compile("(\d+\.\d\d)").findall(result)[0]
    print(result)
    print(value)
    writer.writerow([time,value])
    last_roi=roi

with open('data.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(["time","value"])
    last_roi=[]
    while hasFrames:
        time=count/frameRate
        print("processing frame: "+str(count))
        (W,H,roi,boxes)=get_roi(Image,padding=40)
        out=extract(Image,roi,W,H,count)
       
        try:
            ocr(count,data_writer,time)
            last_roi=roi
        except:
            try:
                out=extract(Image,last_roi,W,H)
                ocr(count,data_writer,time)
            except:
                print("NA")
                data_writer.writerow([time,"NA"])
        hasFrames,Image=vidcap.read()
        count+=1


