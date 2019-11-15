#! /usr/bin/env python3

from lib.get_roi import get_roi
from lib.extract import extract
from lib.process import process
from lib.ocr import ocr
from lib.ocr import NoTextFound
import cv2
import logging
import csv
import traceback

def main(video_file,output_file):
    vidcap = cv2.VideoCapture(video_file)
    frameRate=vidcap.get(cv2.CAP_PROP_FPS)
    hasFrames,Image=vidcap.read()

    count=0
    with open(output_file, mode='w') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(["second_offset","scale_reading"])
        last_roi=None
        while hasFrames:
            time=count/frameRate
            logging.info("processing frame "+str(count))
            cv2.imwrite("./data/images/raw/"+str(count)+".png",Image)  
            
            (W,H,roi,boxes)=get_roi(Image,padding=40)
            extracted_roi=extract(Image,roi,W,H,count)
            black_and_white_roi=process(extracted_roi) 

            try:
                ocr(black_and_white_roi,count,data_writer,time)
                last_roi=roi
            except NoTextFound:
                logging.debug("Could not find text, retrying using last good ROI")
                try:
                    if last_roi:
                        extracted_roi=extract(Image,last_roi,W,H,count)
                        black_and_white_roi=process(extracted_roi) 

                        ocr(black_and_white_roi,count,data_writer,time)
                        last_roi=roi
                    else:
                        logging.debug("No previous ROI, skipping to Next frame")
                except NoTextFound:
                    logging.debug("Still could not find good text, returning NA")
                    data_writer.writerow([time,"NA"])
            hasFrames,Image=vidcap.read()
            count+=1

if __name__== "__main__":
    import argparse

    parser = argparse.ArgumentParser(
            "ssocr-video.py",
            description="Parses the seven segment display data from a video",
            epilog="USAGE: ssocr-video ./data/video.mp4 ./data/output.csv")

    parser.add_argument("video", help="the location of the video", type=str)
    parser.add_argument("output", help="location to write output csv", type=str)
    parser.add_argument("--log", help="logging level", type=str,default="debug")
    args = parser.parse_args()
    
    logging.basicConfig(level=getattr(logging, args.log.upper(), None))
    main(args.video,args.output)
