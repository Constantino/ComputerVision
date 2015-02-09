#!/usr/bin/python

import cv2
from Tkinter import *
from tkFileDialog import *
import sys

debug = 1

if len(sys.argv) > 1:
    debug = int(sys.argv[1])

#Robinson's "5-level" masks
mask = [ 
    [ [-1,0,1],[-2,0,2],[-1,0,1] ], #mask 1
    [ [0,1,2],[-1,0,1],[-2,-1,0] ], #mask 2
    [ [1,2,1],[0,0,0],[-1,-2,-1] ], #mask 3
    [ [2,1,0],[1,0,-1],[0,-1,-2] ], #mask 4
    [ [1,0,-1],[2,0,-2],[1,0,-1] ], #mask 5
    [ [0,-1,-2],[1,0,-1],[2,1,0] ], #mask 6
    [ [-1,-2,-1],[0,0,0],[1,2,1] ], #mask 7
    [ [-2,-1,0],[-1,0,1],[0,1,2] ]  #mask 8
] 

histogram = []

def preProcessImg(imagePath):
    img = cv2.imread(imagePath)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #convert to grayscale
    imgCopy = img
    height, width = img.shape

    return img,imgCopy,height,width

def loadFile():
    fname = ""
    try:
        fname = askopenfilename(filetypes=(("All files", "*.*"),
        ("PNG", "*.png")))

    except ValueError:
        print "Please select an image. Try again..."

    return fname

def applyMasks(pixel,img):

    pixelGradients = [] # used to store the gradients of each pixel 
    indexer = [-pixel[0]+1,-pixel[1]+1] # used to get the equivalent position in the mask

    for i in range(len(mask)):
        gradient = 0
        for r in range(pixel[0]-1, pixel[0]+2): # used for a neighborhood 3x3... I need to improve it
            for c in range(pixel[1]-1,pixel[1]+2):
                gradient += img[r,c]*mask[i][r+indexer[0]][c+indexer[1]] #convolution matrix * each pixel
        
        pixelGradients.append(gradient) #the gradient of the mask applied is stored

    maxGradient = max(pixelGradients) #the gradient of the pixel is the maximum gradient obtained

    return maxGradient


def getThreshold(histogram):
    #Basic global thresholding
    t_new = max(histogram)/2.0 #the threshold should be close to the center
    t_old = 0.0
    mean = [0,0]
    while abs(t_old-t_new) > 0.001: #the loop ends until the difference of the old threshold and the new one is minimum

        if debug:
            print "-> threshold: ",t_new

        mean = getAverages(t_new) #get the average of each side based on the current threshold
        t_old = t_new
        t_new = 0.5*(mean[0]+mean[1]) # get a new threshold by obtaining the average of the means
    
    return t_new

def getAverages(t):
    
    sum_upper = 0
    counter_upper = 0

    sum_down = 0
    counter_down = 0
    for e in histogram:
        if e > t: #sum all the gradients > threshold
            sum_upper += e
            counter_upper += 1
        else: #sum all the gradients < threshold
            sum_down += e
            counter_down += 1

    return [(sum_upper/counter_upper*1.0),(sum_down/counter_down*1.0)] #return means 

def processImage():
    
    if debug:
        print "-> preprocessing the image"

    path = loadFile()

    if path == "":

        if debug:
            print "path: -"

        return

    if debug:
        print "-> path: ", path
        
    img,imgCopy,height,width = preProcessImg(path)

    if debug:
        print "-> height: ",height," width: ",width
        print "-> applying masks to each pixel"

    for y in range(1,height-1,1):
        for x in range(1,width-1,1):
            histogram.append( applyMasks([y,x],img) ) #Apply masks for each pixel and save the gradient in the histogram

    T = getThreshold(histogram)
    
    if debug:
        print "-> showing up borders"

    index_counter = 0
    for r in range(1,height-1,1):
        for c in range(1,width-1,1):

            if histogram[index_counter] > T: #Change the color of the borders, borders in white, everything else in black
                
                imgCopy[r,c] = 255
            else:
                
                imgCopy[r,c] = 0

            index_counter += 1

    cv2.imwrite("img/result.png",imgCopy) #Write a new image

    print "-> image successfully saved at img/result.png"

    del histogram[:] # remove all the elements in the histogram

    print "-> You can choose another image ..."

def main():
    master = Tk()

    f = Frame(master, height=300, width=300)
    f.pack_propagate(0)
    f.pack()

    b = Button(f, text="Load a picture", command = processImage)
    b.pack()

    master.title("Edge detection")
    mainloop()

main()
