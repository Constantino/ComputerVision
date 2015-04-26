import cv2
import numpy as np
from matplotlib import pyplot as plt
from random import choice,randint
import math

imgPath = "test/test004.jpg"
img = cv2.imread(imgPath,0)
imgCopy = cv2.imread(imgPath)

def filter_image(img):
    #Process using Otsu's thresholding after Gaussian filtering                                                                               
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return ret,th
    
def get_contours(th):
    #Find contours based on the threshold obtained
    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_histogram_contours(contours):
    hist_contours = []
    contours_array = []
    for i in range(2,len(contours)):
        if (i%2==0):
            contour = contours[i]
            rect = cv2.minAreaRect(contour)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            side = [ 
                math.hypot(box[1][0] - box[0][0], box[1][1] - box[0][1]), 
                math.hypot(box[3][0] - box[0][0], box[3][1] - box[0][1])
            ]
            area = side[0]*side[1]
            hist_contours.append(float("{0:.2f}".format(area)))
            contours_array.append(box)

    print "hist_contours: ",hist_contours
    return hist_contours,contours_array

def basic_global_thresholding(histogram):
    #Basic global thresholding                                                                                                          
    t_new = max(histogram)/2.0 #the threshold should be close to the center                                                             
    t_old = 0.0
    mean = [0,0]
    T = 0
    while abs(t_old-t_new) > 0.001: #the loop ends until the difference of the old threshold and the new one is minimum                 
                        
        mean = get_averages(histogram,t_new) #get the average of each side based on the current threshold                                     
        t_old = t_new
        t_new = 0.5*(mean[0]+mean[1]) # get a new threshold by obtaining the average of the means                                       
        
        T = t_new/2.5

    return T-T*.75

def discard_contours(histogram,contours,T):
    contours_filtered = []
    for i in range(len(contours)):
        if histogram[i] > T:
            contours_filtered.append(contours[i])
            print "average selected: ",histogram[i]
    return contours_filtered
        

def get_averages(histogram,t):

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

def main():
    ret, th = filter_image(img)
    contours = get_contours(th)

    print "len(contours): ",len(contours)

    hist_c,contours_array = get_histogram_contours(contours)

    t = basic_global_thresholding(hist_c)
    print "t_hist: ",t
    contourBoxes = discard_contours(hist_c,contours_array,t)
    print "contour boxes: ",contourBoxes

    

main()

    
            
            
