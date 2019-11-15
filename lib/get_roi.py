#! /usr/bin/env python3

import time
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
import logging

def decode_predictions(scores, geometry,min_confidence=.8):
	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []

	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the
		# geometrical data used to derive potential bounding box
		# coordinates that surround text
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability,
			# ignore it
			if scoresData[x] < min_confidence:
				continue

			# compute the offset factor as our resulting feature
			# maps will be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)

			# extract the rotation angle for the prediction and
			# then compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)

			# use the geometry volume to derive the width and height
			# of the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]

			# compute both the starting and ending (x, y)-coordinates
			# for the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)

			# add the bounding box coordinates and probability score
			# to our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	# return a tuple of the bounding boxes and associated confidences
	return (rects, confidences)

def get_roi(image,padding=30):
    net = cv2.dnn.readNet("models/frozen_east_text_detection.pb")

    (H, W) = image.shape[:2]
    newH=round(H/32)*32
    newW=round(W/32)*32
    image = cv2.resize(image.copy(), (newW, newH))

    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    blob = cv2.dnn.blobFromImage(image, 1.0, (newW, newH),swapRB=True, crop=False)

    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()
    logging.info("text detection took {:.6f} seconds".format(end - start))

    (rects, confidences) = decode_predictions(scores, geometry,min_confidence=.95)
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    def area(box):
        return (box[2]-box[0])*(box[3]-box[1])
    
    box=list(max(rects,key=area))
    box[0]-=3*padding
    box[1]-=padding
    box[2]+=padding
    box[3]+=padding

    roi=image[box[1]:box[3],box[0]:box[2]]
    return (newW,newH,box,rects)
