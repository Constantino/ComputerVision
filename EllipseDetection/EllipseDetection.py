from random import randint, random
from math import sqrt, ceil, floor, fabs, atan2, cos, sin
import numpy as np
import cv2
from ShapeDetection import ShapeDetection as sd

def getTangent(test):

    point,gradient,angle = test.borderInfo[0]

    print "Point1: ", point

    test.originalImg[point[0],point[1]] = [255,0,0]
    
    print "-> Gradient: ",gradient
    print "-> Angle: ",angle

    beta = .21#90 - abs(angle)

    dx = cos(beta)
    dy = sin(beta)

    print "dx,dy: ",dx,",",dy

    point2 = [round(point[0]-abs(dy)),round(point[1]-abs(dx))]

    print "point2: ",point2

    test.originalImg[point2[0],point2[1]] = [0,255,0]

    cv2.imwrite("Tangents_ellipse.png",test.originalImg)

    return

def testPaintBorders(height,width,test):
    print "-> Painting borders"
    
    for l in test.borderInfo:
        
        coord = l[0]
        if coord[0] < height and coord[1] < width:
            test.originalImg[coord[0],coord[1]] = [0,0,255]
        
            
    cv2.imwrite("Borders_ellipse.png",test.originalImg)


def main():
    
    shapeDetector = sd.ShapeDetection()

    shapeDetector.test.path = "img/ellipse.png"

    figures = shapeDetector.detectFigures()

    width = shapeDetector.test.width
    height = shapeDetector.test.height

    #testPaintBorders(height,width, shapeDetector.test)
    getTangent(shapeDetector.test)
    

main()

