import cv2

def extract(Image,roi,W,H,count,padding=10):
    """Given an Image and a ROI box, resizes image, extacts the ROI, optionaly adds a border padding, and resizes result"""
    
    out_width=150
    out_height=80
    resized_original= cv2.resize(Image,(W,H))
    out=cv2.copyMakeBorder(
        cv2.resize(
            resized_original[roi[1]:roi[3],roi[0]:roi[2]]
            ,(out_width,out_height)),
        padding,padding,padding,padding,cv2.BORDER_CONSTANT,None,(0,0,0)
    )

    return out


