import cv2

def extract(Image,roi,W,H,count,padding=10):
    """Given an Image and a ROI box, resizes image, extacts the ROI with given padding, resizes result, and writes input image and output to files"""
    out=cv2.copyMakeBorder(
        cv2.resize(cv2.resize(Image,(W,H))[roi[1]:roi[3],roi[0]:roi[2]],(150,80)),
        padding,padding,padding,padding,cv2.BORDER_CONSTANT,None,(0,0,0)
    )

    #Images are saved to disk to be used by ssocr binary and to help withd debuging
    cv2.imwrite("./data/images/raw/"+str(count)+".png",Image)  
    cv2.imwrite("./data/images/roi/"+str(count)+".png",process(out))
    return out


