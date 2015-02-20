#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
from ComputerVision.EdgeDetection import EdgeDetection as ed

def getNeighborhood(pixel):

    neighborhood = []

    for i in range(pixel[0]-1,pixel[0]+2):
        for j in range(pixel[1]-1,pixel[1]+2):

            neighborhood.append([i,j])

    return neighborhood


def applyDFS(borders):
    visited = []
    stack = []
    
    point = borders[0]
    
    visited.append(point)
    stack.append(point)

    while stack:

        neighborhood = getNeighborhood(point)

        connexions = []
        for e in neighborhood:
            if e in borders:
                if e not in visited:
                    connexions.append(e)
                    
        if not connexions:
            point = stack.pop()
        else:
            point = max(connexions)
            visited.append(point)
            stack.append(point)
    
    return visited


def paintBorder(test):
    for r in range(1,test.height-1,1):
	for c in range(1,test.width-1,1):
		if [r,c] in test.border:
			test.imgCopy[r,c] = 255
		else:
			test.imgCopy[r,c] = 0

def processImage():
    
    test = ed.EdgeDetection()

    if test.debug:
	print "-> preprocessing the image"

    test.path = loadFile()

	
    test.detectBorders()
    #figure = applyDFS(test.border)

    for r in (1,test.height-1,1):
        for c in (1,test.width-1,1):
            for [r,c] in test.border:
                test.imgCopy[r,c] = 100

    cv2.imwrite("result2.png",test.imgCopy)

    del test.histogram[:] # remove all the elements in the histogram

    print "-> You can choose another image ..."


def loadFile():
    fname = ""
    try:
	fname = askopenfilename(filetypes=(("All files", "*.*"),
	                                   ("PNG", "*.png")))

    except ValueError:
	print "Please select an image. Try again..."

    return fname


master = Tk()

f = Frame(master, height=300, width=300)
f.pack_propagate(0)
f.pack()

b = Button(f, text="Load a picture", command = processImage)
b.pack()

master.title("Edge detection")
mainloop()
