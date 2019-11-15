import subprocess
import logging
import cv2
import re

def ocr(image,count,writer,time):
    """uses ssocr binary to extract text from saved black and white image"""
    
    cv2.imwrite("./data/images/roi/"+str(count)+".png",image)
    
    result = subprocess.run(
            'ssocr -d -1 -c decimal -r 3 data/images/roi/%s.png'%(count), 
            shell=True,
            stdout=subprocess.PIPE)
    
    result=str(result.stdout)
    logging.debug("ssocr output: %s"%(result))
    
    value=re.compile("(\d+\.\d\d)").findall(result)[0]
    logging.debug("ssocr output parsed as: %s"%(value))
    
    writer.writerow([time,value])


