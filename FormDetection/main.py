#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
from ComputerVision.EdgeDetection import EdgeDetection as ed


myBackground = 0

def getNeighborhood(test,pixel):

    neighborhood = []

    for i in range(pixel[0]-1,pixel[0]+2):
        for j in range(pixel[1]-1,pixel[1]+2):
            if i < test.height and j < test.width and i > 0 and j > 0:

                neighborhood.append([i,j])

    return neighborhood

def getRidOfBackground(test,borders):
    background = applyDFS(borders,False)

    for e in background:
        test.imgCopy[e] = 80

def isColor(pixel,color):
    print "pixel: ",pixel
    print "color: ",color
    pixelColor = str(pixel[0])+str(pixel[1])+str(pixel[2])
    return pixelColor == color

def getBackground(test):
    colors = {}
    myBackground = {'color': 0, 'frecuency':0}

    for r in range(test.height-1):
        for c in range(test.width-1):
            pixelColor = str(test.originalImg[r,c][0])+str(test.originalImg[r,c][1])+str(test.originalImg[r,c][2])

            if pixelColor not in colors:

                colors[pixelColor] = 1

                if myBackground['color'] == 0:
                    myBackground['color'] = pixelColor
                    myBackground['frequency'] = 1
            else:
                colors[pixelColor] += 1

                if colors[pixelColor] > myBackground['frequency']:
                    myBackground['color'] = pixelColor
                    myBackground['frequency'] = colors[pixelColor]

    return myBackground['color']


def applyDFS(test,borders,myBackground):
    visited = []
    stack = []
    point = []
    
    point = borders[0]
    
    visited.append(point)
    stack.append(point)

    while stack:

        neighborhood = getNeighborhood(test,point)

        connexions = []
        for e in neighborhood:

            if e in borders or not isColor(test.originalImg[e[0],e[1]], str(myBackground)):
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

    myBackground = getBackground(test)
    print "background: ", myBackground
    #getRidOfBackground(test,test.border)

    
    figure = applyDFS(test,test.border,myBackground)
    
    for r in (1,test.height-1,1):
        for c in (1,test.width-1,1):
            for [r,c] in figure:
                test.imgCopy[r,c] = 100
    
    #for e in figure:
    #    test.imgCopy[e] = 100

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
