#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *

from ShapeDetection import ShapeDetection as sd
import random

def execute():
    
    shapeDetector = sd.ShapeDetection()

    shapeDetector.test.path = loadFile()
    
    figures = shapeDetector.detectFigures()
    
    shapeDetector.drawBoundingBox(figures)

    cv2.imwrite("result2.png",shapeDetector.test.originalImg)

    del shapeDetector.test.histogram[:] # remove all the elements in the histogram

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

b = Button(f, text="Load a picture", command = execute)
b.pack()

master.title("Edge detection")
mainloop()
