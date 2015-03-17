from random import randint, random
from math import sqrt, ceil, floor, fabs, atan2, cos, sin
import numpy as np
import cv2
from ShapeDetection import ShapeDetection as sd

def circleEquation(x,xc,y,yc,r):
	c = (x-xc)**2 + (y-yc)**2
	r2 = r**2
	# r2-200 <= c <= r2
	return  c <= r2  and c >= (r2-200)

def applyDGMasks(img,heigh,width,mask,border):
		print "applying DG mask"
		Gx = []
		Gy = []
		for y in range(1,height-1,1):

			for x in range(1,width-1,1):
				if [y,x] in border:
					pixelGradients = []

					# used to get the equivalent position in the mask
					indexer = [-y+1,-x+1] 
		
					for i in range(len(mask)):
						gradient = 0
						# used for a neighborhood 3x3... I need to improve it
						for r in range(y-1, y+2): 
						    for c in range(x-1,x+2):
							#convolution matrix * each pixel
							gradient += img[r,c]*mask[i][r+indexer[0]][c+indexer[1]] 

						#the gradient of the mask applied is stored
						pixelGradients.append(gradient) 

					Gx.append(pixelGradients[0])
					Gy.append(pixelGradients[1])
		
		return Gx,Gy




mask = [
	[ [-1,0,1], [-2,0,2], [-1,0,1] ],
	[ [1,2,1], [0,0,0], [-1,-2,-1] ]
]

#starting
shapeDetector = sd.ShapeDetection()
shapeDetector.test.path = "CircleDetection/c.png"
shapeDetector.test.detectBorders()
#figures = shapeDetector.detectFigures()
#shapeDetector.drawBoundingBox(shapeDetector.test.border)
height = shapeDetector.test.height
width = shapeDetector.test.width

for pixel in shapeDetector.test.border:

	shapeDetector.test.originalImg[pixel[0],pixel[1]] = [0,0,255]


i = shapeDetector.test.border
i.sort()
n_elem = len(i)
print "i[0][0]: ",i[0][0]
y_min = i[0][0]
y_max = i[n_elem-1][0]
x_min =  i[n_elem-1][1]
x_max = 0

sum_x = 0
sum_y = 0

for e in i:
    sum_x += e[1]
    sum_y += e[0]

    if e[1] > x_max:
        x_max = e[1]
    if e[1] < x_min:
        x_min = e[1]

color = [0,255,0]

for z in range(x_min,x_max+1):
    shapeDetector.test.originalImg[y_min,z] = color
    shapeDetector.test.originalImg[y_max,z] = color
for z in range(y_min,y_max+1):
    shapeDetector.test.originalImg[z,x_min] = color
    shapeDetector.test.originalImg[z,x_max] = color

centerOfMass = [sum_y/n_elem,sum_x/n_elem]
radio = centerOfMass[1] - x_min

for y in xrange(centerOfMass[0]-1,centerOfMass[0]+2,1):
	for x in xrange(centerOfMass[1]-1,centerOfMass[1]+2,1):
		shapeDetector.test.originalImg[y,x] = [0,0,255]

Gx,Gy = applyDGMasks(shapeDetector.test.imgCopy,height,width,mask,shapeDetector.test.border)

print "Gx: "
print Gx
print "Gy: "
print Gy

print "x_min: ",x_min," centerOfMass: ",centerOfMass," radio: ",radio

votes = dict()

for i in range(len(shapeDetector.test.border)):
	p = shapeDetector.test.border[i]
	shapeDetector.test.originalImg[p[0],p[1]] = [255,0,0]
	g = sqrt( Gx[i]**2 + Gy[i]**2 )
	cosTheta = Gx[i] / g
	sinTheta = Gy[i] / g
	angle = atan2(Gy[i],Gx[i])
	xc = int(round(p[1] - radio * cosTheta))
	yc = int(round(p[0] - radio * sinTheta))
	
	if xc >= 0 and xc < x_max and yc >= 0 and yc < y_max:
		shapeDetector.test.originalImg[yc,xc] = [0,255,255]
		vote = str(yc)+","+str(xc)
		if vote not in votes:
			votes[vote] = 1
		else:
			votes[vote] += 1
bigger = ""
for v in votes:
	if bigger == "":
		bigger = v
	elif votes[v] > votes[bigger]:
		bigger = v

print bigger
biggers = list()
print "votes:  ",votes
print "votes >= 4: "

for v in votes:
	if votes[v] >= 4:
		print "votes[",v,"] :",votes[v]
		biggers.append([int(v[0]+v[1]),int(v[3]+v[4])])

yc_d = int(bigger[0]+bigger[1])
xc_d = int(bigger[3]+bigger[4])
"""
for y in xrange(yc_d-1,yc_d+2,1):
	for x in xrange(xc_d,xc_d+2,1):
		shapeDetector.test.originalImg[y,x] = [0,0,0]
"""
for p in biggers:
	shapeDetector.test.originalImg[p[0],p[1]] = [0,0,0]


sum_x = 0
sum_y = 0

for e in biggers:
    sum_x += e[1]
    sum_y += e[0]

lenght = len(biggers)
center_c_d = [int(round(sum_y/lenght)),int(round(sum_x/lenght))]

for y in xrange(center_c_d[0]-1,center_c_d[0]+2,1):
	for x in xrange(center_c_d[1],center_c_d[1]+2,1):
		shapeDetector.test.originalImg[y,x] = [0,0,0]

print "borde 0: ",shapeDetector.test.border[0]
"""
for pixel in shapeDetector.test.border:
	shapeDetector.test.originalImg[pixel[0],pixel[1]] = [0,0,255]
"""
newRadio = center_c_d[1] - x_min
for y in range(1,height-1,1):
	for x in range(1,width-1,1):
		if circleEquation(x,center_c_d[1],y,center_c_d[0],newRadio):
			shapeDetector.test.originalImg[y,x] = [0,140,255]


cv2.imwrite("result_Circle.png",shapeDetector.test.originalImg)

