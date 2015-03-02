#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
#from EdgeDetection import EdgeDetection as ed
from ShapeDetection import ShapeDetection as sd
import math

def groupByAngle():
    
    for e in shapeDetector.test.border:
        indexCounter = 0
        for r in range(1,shapeDetector.test.height-1,1):
            for c in range(1,shapeDetector.test.width-1,1):
                print shapeDetector.test.angles[indexCounter]
                
                if shapeDetector.test.angles[indexCounter] == 0:
                    groups[0].append([r,c])
                elif shapeDetector.test.angles[indexCounter] == 45:
                    groups[1].append([r,c])
                elif shapeDetector.test.angles[indexCounter] == 90:
                    groups[2].append([r,c])
                elif shapeDetector.test.angles[indexCounter] == -45:
                    groups[3].append([r,c])

                indexCounter += 1
                

def getFromGroup():
    detect = shapeDetector.applyDFS(shapeDetector.test,groups[0],background)
    return detect
    """
    for i in detect:
        shapeDetector.test.originalImg[i[0],i[1]] = [0,0,255]

    cv2.imwrite("lines_Test.png",shapeDetector.test.originalImg)
    """

def calcDistributionOfSizes():
    return

def discardLittleLines():
    return

histogram = []
c = {}
def getEquation(point,angle=0):
    
    #for angle in range(0,180,10):
    p = point[0]*math.cos(angle) + point[1]*math.sin(angle)

    if [p,angle] not in histogram:
        histogram.append([p,angle])
        c[str(round(p))+","+str(angle)] = 0
    else:
        c[str(round(p))+","+str(angle)] += 1


def drawLines():
    return


shapeDetector = sd.ShapeDetection()
shapeDetector.test.path = "LineDetection/figures.png"
shapeDetector.test.detectBorders()
background = shapeDetector.getBackground()

#         0  45 90 -45                                                                                                                         
groups = [[],[],[],[]]

def main():
    groupByAngle()

    pointsGrouped = getFromGroup()

    for point in pointsGrouped:
        getEquation(point)

    maxValue = 0
    keyChosen = ""

    print c

    for key,value in c.items():
        if value > maxValue:
            maxValue = value
            keyChosen = key

    print "key: ",key," value: ",value
    

main()
