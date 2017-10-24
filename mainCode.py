/*
openface installation link for unix:
https://github.com/TadasBaltrusaitis/OpenFace/wiki/Unix-Installation
*/

import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import os
from PIL import Image
import sys

#path = "/home/MainCode"
path = "path of code"

"""Extracting desired landmarks from the default file obtained from openface and saving in output file"""
f = open(path+"/defaultFiles/default1.txt", "r")
out = open(path+"/outputFiles/output1.txt", "w")
lines = f.readlines()

for x in lines:
    out.write(x.split(' ')[0]+" "+
		
	x.split(' ')[52]+" "+x.split(' ')[120]+" "+
	x.split(' ')[53]+" "+x.split(' ')[121]+" "+
	x.split(' ')[54]+" "+x.split(' ')[122]+" "+
	x.split(' ')[55]+" "+x.split(' ')[123]+" "+
	x.split(' ')[56]+" "+x.split(' ')[124]+" "+
	x.split(' ')[57]+" "+x.split(' ')[125]+" "+

    	x.split(' ')[58]+" "+x.split(' ')[126]+" "+
    	x.split(' ')[59]+" "+x.split(' ')[127]+" "+ 
    	x.split(' ')[60]+" "+x.split(' ')[128]+" "+
    	x.split(' ')[61]+" "+x.split(' ')[129]+" "+
    	x.split(' ')[62]+" "+x.split(' ')[130]+" "+
    	x.split(' ')[63]+" "+x.split(' ')[131]+" "+
    	" "+"\n") 
f.close()
out.close()

infile = open(path+"/outputFiles/output1.txt", "r+")
outfile = open(path+"/outputFiles/outfile_test_1.txt", "w")
"""------------------Removing commas--------------------"""
temp = infile.read().replace(",", "")
outfile.write(temp)
outfile.close()
infile.close()

file = open(path+"/outputFiles/outfile_test_1.txt", "r")
lines = file.readlines()
print len(lines)

"""--------------------frame capturing------------------------"""
vidcap = cv2.VideoCapture(path+"/video/1.webm")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
"""---------------------Creating output video-------------------------"""
output = cv2.VideoWriter(path + '/OutputVideos/outVideo1.avi',fourcc,20.0,(1280,1024))
success,image = vidcap.read()
print "success",success
success = True

count = 1
while success:
	success, frame = vidcap.read()
	"""eye coordinates for one eye"""
	y1 = int(float(lines[count].split(' ')[4]))
	y2 = int(float(lines[count].split(' ')[10]))
	x1 = int(float(lines[count].split(' ')[1]))
	x2 = int(float(lines[count].split(' ')[7]))

	"""eye coordinates for second eye"""
	Y1 = int(float(lines[count].split(' ')[16]))
	Y2 = int(float(lines[count].split(' ')[22]))
	X1 = int(float(lines[count].split(' ')[13]))
	X2 = int(float(lines[count].split(' ')[19]))
	
	#crop_img = img[(y1 of 37):(y2 of 40),(x1 of 36):(x2 of 39)]
	"""cropped image of one eye"""
	crop_img = frame[(y1):(y2) , (x1):(x2)]
	"""cropped image of second eye"""
	crop_img2 = frame[(Y1):(Y2) , (X1):(X2)]
	#cv2.imshow("crop_img",crop_img)
	crop_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	crop_gray2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)
	
	#applying threshold
	ret,thresh = cv2.threshold(crop_gray,85,255,cv2.THRESH_BINARY)
	ret,thresh2 = cv2.threshold(crop_gray2,85,255,cv2.THRESH_BINARY)
	#cv2.imshow("thresh",thresh)

	cv2.imwrite(path+'/croppedImages/t.jpg',thresh)
	img = Image.open(path+'/croppedImages/t.jpg').convert('1')

	cv2.imwrite(path+'/croppedImages/t2.jpg',thresh2)
	img2 = Image.open(path+'/croppedImages/t2.jpg').convert('1')
	
	img = img.resize((80,35), Image.ANTIALIAS)
	pixels = img.load()
	width , height = img.size

	img2 = img2.resize((80,35), Image.ANTIALIAS)
	pixels2 = img2.load()
	width2 , height2 = img2.size

	xtotal = 0
	ytotal = 0
	total  = 0

	xtotal2 = 0
	ytotal2 = 0
	total2 = 0

	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixels[x, y] == 0:
				xtotal += x
				ytotal += y
				total += 1

	for y in xrange(img2.size[1]):
		for x in xrange(img2.size[0]):
			if pixels2[x, y] == 0:
				xtotal2 += x
				ytotal2 += y
				total2 += 1				
	
	if xtotal > 0 and ytotal > 0:
		xtotal /= total
		ytotal /= total

	if xtotal2 > 0 and ytotal2 > 0:
		xtotal2 /= total2
		ytotal2 /= total2

	"""xtotal and ytotal calculates the average of black pixels where the iris is"""
	print "x1 = ",xtotal," y1 = ",ytotal
	print "x2 = ",xtotal2," y2 = ",ytotal2
 
	cv2.circle(frame,(xtotal+x1,ytotal+y1), 5, (100,0,255),-1)
	cv2.circle(frame,(xtotal2+X1-8,ytotal2+Y1), 5, (100,0,255),-1)

	cv2.imshow("thresh",frame)
	
	font = cv2.FONT_HERSHEY_SIMPLEX

	if xtotal >= 0 and xtotal <= 28:		
		cv2.putText(frame,'LEFT',(50,100), font, 4,(0,0,255),2)

	if xtotal >= 29 and xtotal <= 45:
		cv2.putText(frame,'CENTER',(50,100), font, 4,(0,0,255),2)
	
	if xtotal >= 46 and xtotal <= 80:
		cv2.putText(frame,'RIGHT',(50,100), font, 4,(0,0,255),2)
	output.write(frame)
	count += 1

vidcap.release()
cv2.destroyAllWindows()
