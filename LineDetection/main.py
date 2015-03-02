#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
from EdgeDetection import EdgeDetection as ed

test = ed.EdgeDetection()
test.path = "figures.png"
borders = test.detectBorders()

#         0  45 90 -45
groups = [[],[],[],[]]

def groupByAngle(test):
    
    for e in test.border:
        indexCounter = 0
        for r in range(1,test.height-1,1):
            for c in range(1,test.width-1,1):
                
                if test.angles[indexCounter] == 0:
                    groups[0].append([r,c])
                elif test.angles[indexCounter] == 45:
                    groups[1].append([r,c])
                elif test.angles[indexCounter] == 90:
                    groups[2].append([r,c])
                elif test.angles[indexCounter] == -45:
                    groups[3].append([r,c])

def getFromGroup():
    return

def calcDistributionOfSizes():
    return

def discardLittleLines():
    return

def getEquation():
    return

def drawLines():
    return


