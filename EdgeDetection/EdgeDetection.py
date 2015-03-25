import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
import math

class EdgeDetection:
	
	def __init__(self):
		self.debug = 1

		if len(sys.argv) > 1:
		    self.debug = int(sys.argv[1])
                    
		self.originalImg = None
		self.imgCopy = None
		self.height = None
		self.width = None
		self.path = None
		self.T = None
                
		#Robinson's "5-level" masks
		self.mask = [ 
		    [ [-1,0,1],[-2,0,2],[-1,0,1] ], #mask 1
		    [ [0,1,2],[-1,0,1],[-2,-1,0] ], #mask 2
		    [ [1,2,1],[0,0,0],[-1,-2,-1] ], #mask 3
		    [ [2,1,0],[1,0,-1],[0,-1,-2] ], #mask 4
		    [ [1,0,-1],[2,0,-2],[1,0,-1] ], #mask 5
		    [ [0,-1,-2],[1,0,-1],[2,1,0] ], #mask 6
		    [ [-1,-2,-1],[0,0,0],[1,2,1] ], #mask 7
		    [ [-2,-1,0],[-1,0,1],[0,1,2] ]  #mask 8
		] 
		
		#Sobel's mask for DG
		self.DGMasks = [
			[ [-1,0,1], [-2,0,2], [-1,0,1] ],
			[ [1,2,1], [0,0,0], [-1,-2,-1] ]
		]

		self.histogram = []
		self.border = []
                self.angles = []
                self.borderInfo = []

	def preProcessImg(self,imagePath):
	    self.originalImg = cv2.imread(imagePath)
	    self.img = cv2.cvtColor(self.originalImg,cv2.COLOR_RGB2GRAY) #convert to grayscale
	    self.imgCopy = self.img
	    self.height, self.width = self.img.shape
            if self.debug:
	    	print "-> height: ",self.height," width: ",self.width
		print "-> applying masks to each pixel"

	def applyMasks(self,pixel,img):

	    pixelGradients = [] # used to store the gradients of each pixel 
	    indexer = [-pixel[0]+1,-pixel[1]+1] # used to get the equivalent position in the mask

	    for i in range(len(self.mask)):
		gradient = 0
		for r in range(pixel[0]-1, pixel[0]+2): # used for a neighborhood 3x3... I need to improve it
		    for c in range(pixel[1]-1,pixel[1]+2):
		        gradient += img[r,c]*self.mask[i][r+indexer[0]][c+indexer[1]] #convolution matrix * each pixel
		        
		pixelGradients.append(gradient) #the gradient of the mask applied is stored

	    maxGradient = max(pixelGradients) #the gradient of the pixel is the maximum gradient obtained

            self.angles.append(self.setAngles(pixelGradients,maxGradient))

	    return maxGradient
	
	def applyDGMasks(self,pixel,img):
		pixelGradients = []
		indexer = [-pixel[0]+1,-pixel[1]+1] # used to get the equivalent position in the mask
		
		for i in range(len(self.mask)):
			gradient = 0
			for r in range(pixel[0]-1, pixel[0]+2): # used for a neighborhood 3x3... I need to improve it
			    for c in range(pixel[1]-1,pixel[1]+2):
				gradient += img[r,c]*self.mask[i][r+indexer[0]][c+indexer[1]] #convolution matrix * each pixel

			pixelGradients.append(gradient) #the gradient of the mask applied is stored

		maxGradient = abs(pixelGradients[0]) + abs(pixelGradients[1])
		angle = math.atan2(pixelGradients[1],pixelGradients[0])

		return maxGradient,angle

        def setAngles(self,pixelGradients,maxGradient):

           index = pixelGradients.index(maxGradient) + 1

           if index == 1 or index == 5:
               return 90
           elif index == 2 or index == 6:
               return 45
           elif index == 3 or index == 7:
               return 0
           else:
               return -45

	def getThreshold(self,histogram):
	    #Basic global thresholding
	    t_new = max(histogram)/2.0 #the threshold should be close to the center
	    t_old = 0.0
	    mean = [0,0]
	    while abs(t_old-t_new) > 0.001: #the loop ends until the difference of the old threshold and the new one is minimum

		if self.debug:
		    print "-> threshold: ",t_new

		mean = self.getAverages(t_new) #get the average of each side based on the current threshold
		t_old = t_new
		t_new = 0.5*(mean[0]+mean[1]) # get a new threshold by obtaining the average of the means

	    self.T = t_new/2.5 
	    if self.debug:
		print "-> Final Threshold: ",self.T
		
	    return self.T #We get a better border clearly defined by divinding the final Threshold into 2.5

	def getAverages(self,t):
	    
	    sum_upper = 0
	    counter_upper = 0

	    sum_down = 0
	    counter_down = 0
	    for e in self.histogram:
		if e > t: #sum all the gradients > threshold
		    sum_upper += e
		    counter_upper += 1
		else: #sum all the gradients < threshold
		    sum_down += e
		    counter_down += 1

	    return [(sum_upper/counter_upper*1.0),(sum_down/counter_down*1.0)] #return means 
	
	def getBorders(self, T):
		    index_counter = 0
		    for r in range(1,self.height-1,1):
			for c in range(1,self.width-1,1):
			    #Change the color of the borders, borders in white, everything else in black
			    if self.histogram[index_counter] > T:
				
				for i in range(r-1,r+2): #big border painting the neighborhood for each pixel border detected
				    for j in range(c-1,c+2):
					self.border.append([i,j])
                                        self.borderInfo.append([ [i,j],self.histogram[index_counter],self.angles[index_counter] ])

			    index_counter += 1

	def detectBorders(self):
	    self.preProcessImg(self.path)
	    for y in range(1,self.height-1,1):
		for x in range(1,self.width-1,1):
		    gradient,angle = self.applyDGMasks([y,x],self.img)
		    self.histogram.append(gradient) #Apply masks for each pixel and save the gradient in the histogram
                    #self.borderInfo.append([ [y,x],gradient,angle ])
		    self.angles.append(angle)

	    self.T = self.getThreshold(self.histogram)
	    self.getBorders(self.T)
