#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
#from EdgeDetection import EdgeDetection as ed
from ShapeDetection import ShapeDetection as sd

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
    #detect = shapeDetector.applyDFS(shapeDetector.test.border,background)

def calcDistributionOfSizes():
    return

def discardLittleLines():
    return

def getEquation():

    

    return

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

    getFromGroup()


main()
