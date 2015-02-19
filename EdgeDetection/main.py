#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
from EdgeDetection import EdgeDetection


def paintBorder(test):
    for r in range(1,test.height-1,1):
	for c in range(1,test.width-1,1):
		if [r,c] in test.border:
			test.imgCopy[r,c] = 255
		else:
			test.imgCopy[r,c] = 0

def processImage():
    
    test = EdgeDetection()

    if test.debug:
	print "-> preprocessing the image"

    test.path = loadFile()

    if test.path == "":

	if test.debug:
	    print "path: -"

	return

    if test.debug:
	print "-> path: ", test.path
	
    test.detectBorders()

    if test.debug:
	print "-> showing up borders"


    paintBorder(test)
	    
    cv2.imwrite("img/result.png",test.imgCopy) #Write a new image

    print "-> image successfully saved at img/result.png"

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
