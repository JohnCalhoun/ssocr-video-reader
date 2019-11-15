#! /usr/bin/env python3

from lib.get_roi import get_roi
from lib.extract import extract
from lib.process import process
from lib.ocr import ocr
import cv2
import logging
import csv
import traceback

def main(video_file,output_file):
    vidcap = cv2.VideoCapture(video_file)
    frameRate=vidcap.get(cv2.CAP_PROP_FPS)
    hasFrames,Image=vidcap.read()

    count=0
    with open('data.csv', mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(["second_offset","scale_reading"])
        last_roi=[]
        while hasFrames:
            time=count/frameRate
            logging.info("processing frame "+str(count))
            (W,H,roi,boxes)=get_roi(Image,padding=40)
            out=extract(Image,roi,W,H,count)
           
            try:
                ocr(count,data_writer,time)
                last_roi=roi
            except NameError as e_1:
                logging.debug("Could not find text, retrying using last good ROI")
                try:
                    out=extract(Image,last_roi,W,H,count)
                    ocr(count,data_writer,time)
                    last_roi=roi
                except NameError as e_2:
                    logging.debug("Still could not find good text, returning NA")
                    data_writer.writerow([time,"NA"])
            hasFrames,Image=vidcap.read()
            count+=1

if __name__== "__main__":
    import argparse

    parser = argparse.ArgumentParser("ssocr-video.py",description="Parses the seven segment display data from a video")
    parser.add_argument("video", help="the location of the video", type=str)
    parser.add_argument("output", help="location to write output csv", type=str)
    parser.add_argument("--log", help="logging level", type=str,default="debug")
    args = parser.parse_args()
    
    logging.basicConfig(level=getattr(logging, args.log.upper(), None))
    main(args.video,args.output)
