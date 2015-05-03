import cv2
import numpy as np
from matplotlib import pyplot as plt
from random import choice,randint
import math

imgPath = "test/test008.jpg"
img = cv2.imread(imgPath,0)
imgCopy = cv2.imread(imgPath)
height, width = img.shape

def filter_image(img):
    #source: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#thresholding
    #Process using Otsu's thresholding after Gaussian filtering                                                                               
    blur = cv2.GaussianBlur(img,(5,5),0)
    
    cv2.imwrite('blur.png',blur)
    ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return ret,th
    
def get_contours(th):
    #Find contours based on the threshold obtained
    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_histogram_contours(contours):
    hist_contours = []
    contours_array = []
    
    for i in range(len(contours)):
        
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

    return T-T*.95

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

def draw_bounding_boxes(contourBoxes,thickness):

    for e in contourBoxes:
        color = [randint(100,255),randint(0,150),randint(0,255)]
        cv2.drawContours(imgCopy,[e],0,color,thickness)
        #draw_corner_points(e,thickness,0)

def draw_corner_points(box,thickness,black):
    
    colors = [[0,0,255],[0,255,0],[255,0,0],[155,155,155]]
    counter = 0
    for e in box:
        color_box = [randint(100,255),randint(0,150),randint(0,255)]
        for x in range(e[0]-thickness,e[0]+thickness):
            for y in range(e[1]-thickness,e[1]+thickness):
                if x < width and y < height:
                    if black:
                        imgCopy[y,x] = [0,0,0]
                    else:
                        imgCopy[y,x] = [0,255,0]
                        
                        

def get_reference_object(contours):
    shape_colors = []
    for e in contours:
        colors = []
        for x in range(e[1][0],e[2][0]):
            for y in range(e[1][1],e[3][1]):
                colors.append([imgCopy[y,x][0],imgCopy[y,x][1],imgCopy[y,x][2]])
        shape_colors.append(colors)

    counter = []
    for e in shape_colors:
        counter_sc = 0
        for i in e:
            
            if i[2] > 100 and i[1] < 100 and i[0] < 100:
                counter_sc += 1

        counter.append(counter_sc)
    
    print "Counter-colors-shape: ",counter

    max_value = max(counter)
    shape_index = -1
    for i in range(len(counter)):
        if counter[i] == max_value:
            shape_index = i

    print "shape index: ",shape_index

def transform(img,box):
    rows,cols = img.shape[:2]
    #print "box to perspective: ",box[0]," ",box[1]," "," ",box[2]," ",box[3]
    print "BOX: ",box
    print "box to trans: ",box[1],box[2],box[0],box[3]
    #pts1 = np.float32([box[1],box[2],box[0],box[3]])
    pts1 = np.float32([box[0],box[1],box[3],box[2]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    
    dst = cv2.warpPerspective(img,M,(640,480))
    return dst

def order_points(pts):
    #source: http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")
    #rect = []
    
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    print "np.argmin(pts,1): ",np.argmin(s)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts)
    print "diff: ",diff
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
 
    # return the ordered coordinates
    return rect

def main():
    ret, th = filter_image(img)

    cv2.imwrite('RESULT_0.png',th)

    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print "Contours: ",contours
    
    print "len(contours): ",len(contours)

    hist_c,contours_array = get_histogram_contours(contours)
    
    t = basic_global_thresholding(hist_c)
    print "t_hist: ",t
    contourBoxes = discard_contours(hist_c,contours_array,t)
    print "contour boxes: ",contourBoxes

    cv2.drawContours(imgCopy,contourBoxes,-1,[0,0,255],15)

    cv2.imwrite('RESULT.png',imgCopy)

main()



    
            
            
