from random import randint, random
from math import sqrt, ceil, floor, fabs, atan2, cos, sin, pi
import numpy as np
import cv2
from ShapeDetection import ShapeDetection as sd

def getTangent(test):

    for item in test.borderInfo:
        point,gradient,angle = item#test.borderInfo[300]

        print "Point1: ", point

        test.originalImg[point[0],point[1]] = [255,0,0] #Paint point 1
    
        print "-> Gradient: ",gradient
        print "-> Angle: ",angle

        beta = 3.1416/2-angle #90 - abs(angle)
        print "beta: ", beta
        dx = cos(beta)
        dy = sin(beta)

        m = dy/dx

        print "dx,dy: ",dx,",",dy
        print "m: ",m

        for r in xrange(test.height):
            for c in xrange(test.width):
                y = int(round(m*(c-point[1])+point[0]))
                #print "y: ",y
                if y >= 0 and y < test.height:
                    test.originalImg[y,c] = [0,255,0]

        """
        point2 = [int(round(m*(point[1]-5 - point[1]))),point[1]]

        print "point2: ",point2

        test.originalImg[point2[0],point2[1]] = [0,255,0] #Paint point 2
        """
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

