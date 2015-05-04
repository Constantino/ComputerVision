import cv2
import numpy as np
from matplotlib import pyplot as plt
from random import choice,randint
import math

global img #= cv2.imread(imgPath,0)
global imgCopy #= cv2.imread(imgPath)
global height, width #= img.shape

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

    #print "hist_contours: ",hist_contours
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
            #print "average selected: ",histogram[i]
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

def draw_bounding_boxes(imgCopy,contourBoxes,thickness):
    counter = 0
    for e in contourBoxes:
        color = [randint(100,255),randint(0,150),randint(0,255)]
        cv2.drawContours(imgCopy,[e],-1,color,thickness)
        set_label(imgCopy,"Shape "+str(counter), e[1])
        counter+=1
        

def set_label(imgCopy,text,coordinate):
    label = text
    cv2.putText(imgCopy,label, (coordinate[0], coordinate[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (70,70,240),5)


def draw_corner_points(imgCopy,box,thickness,black):
    
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
                        
                        

def get_reference_objectByColor(imgCopy,contours):
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
    
    #print "Counter-colors-shape: ",counter

    max_value = max(counter)
    shape_index = -1
    for i in range(len(counter)):
        if counter[i] == max_value:
            shape_index = i

    #print "shape index: ",shape_index

def getLimits(box):
    xmin = box[0][0]
    xmax = box[0][0]
    ymin = box[0][1]
    ymax = box[0][1]

    for e in box:
        if e[0] < xmin:
            xmin = e[0]
        if e[0] > xmax:
            xmax = e[0]
        if e[1] < ymin:
            ymin = e[1]
        if e[1] > ymax:
            ymax = e[1]
    #print "xmin,xmax,ymin,ymax: ",xmin,xmax,ymin,ymax
    return xmin,xmax,ymin,ymax

def getReferenceObject(coord,contourBoxes,scaleW,scaleH):
    print "coord: ",coord
    coord = coord[0]*scaleW,coord[1]*scaleH
    resultImg = cv2.imread("RESULT.png")
    found = False
    index = -1
    counter = 0
    for box in contourBoxes:
        xmin,xmax,ymin,ymax = getLimits(box)
        #print "BOX: ",box
        if xmin < coord[0] and ymin < coord[1] and  coord[0] < xmax and coord[1] < ymax :
            #print "coord in box - "
            found = True
            index = counter
            cv2.drawContours(resultImg,[box],-1,(0,0,255),25)

        else:
            #print "coord NOT IN box -"
            cv2.drawContours(resultImg,[box],-1,(255,0,0),25)        

        counter += 1
        print "validation: ",(xmin,ymin)," - ",(xmax,ymax), "coord: ",coord

    cv2.imwrite("RESULT.png",resultImg)

    return found,index

def DrawPoint(point,scaleW,scaleH):
    point = int(point[0]*scaleW),int(point[1]*scaleH)
    resultImg = cv2.imread("RESULT.png")
    cv2.circle(resultImg,point,20,(0,255,0),15)
    cv2.imwrite("RESULT.png",resultImg)
    
def MeasureLine(contourBoxes,objectIndex,point1,point2,scaleW,scaleH,unit):
    resultImg = cv2.imread("RESULT.png")

    box = contourBoxes[objectIndex]
    boxDist = math.hypot(box[1][0] - box[0][0], box[1][1] - box[0][1])
    
    point1 = int(point1[0]*scaleW),int(point1[1]*scaleH)
    point2 = int(point2[0]*scaleW),int(point2[1]*scaleH)
    
    dist = math.hypot(abs(point1[0]-point2[0]),abs(point1[1]-point2[1]))
    baseMeasure = 4.0#cm
    inches = 0.393700787
    distR = (dist*baseMeasure/boxDist)
    label = str(float("{0:.1f}".format(distR*inches)))
                    
    label = label+" in"

    cv2.line(resultImg, (point1), (point2), (0,255,0),10)
    cv2.putText(resultImg,label,point1, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,250),5)

    cv2.imwrite("RESULT.png",resultImg)

def Measure(objectIndex,contourBoxes,unit):
    dist = []
    box = contourBoxes[objectIndex]
    dist.append(math.hypot(box[1][0] - box[0][0], box[1][1] - box[0][1])) 
    dist.append(math.hypot(box[3][0] - box[0][0], box[3][1] - box[0][1]))
    baseMeasure = 4.0 #cm

    resultImg = cv2.imread("RESULT.png")

    for i in range(len(contourBoxes)):
        if i != objectIndex or 1 == 1:
            
            boxDist = []
            boxToMeasure = contourBoxes[i]
            boxDist.append(math.hypot(boxToMeasure[1][0] - boxToMeasure[0][0], boxToMeasure[1][1] - boxToMeasure[0][1])) 
            boxDist.append(math.hypot(boxToMeasure[3][0] - boxToMeasure[0][0], boxToMeasure[3][1] - boxToMeasure[0][1]))

            

            width = boxDist[0]*baseMeasure/dist[0]
            height = boxDist[1]*baseMeasure/dist[1]

            label1 = str(float("{0:.1f}".format(height)))
            label2 = str(float("{0:.1f}".format(width)))
            
            if unit == "cm":
                label = label1 + " X " + label2+" cm"
            else:
                if unit == "in":
                    inches = 0.393700787
                    label1 = str(float("{0:.1f}".format(height*inches)))
                    label2 = str(float("{0:.1f}".format(width*inches)))
                
                if unit == "mm":
                    mm = 10
                    label1 = str(float("{0:.1f}".format(height*mm)))
                    label2 = str(float("{0:.1f}".format(width*mm)))

                label = label1 + " X "+label2+" "+unit

            labelSize = len(label)*15
            xmin,xmax,ymin,ymax = getLimits(boxToMeasure)
            cv2.putText(resultImg,label, (xmin + int(abs(xmax-xmin)/2)-labelSize,ymin+int(abs(ymax-ymin)/2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,130,255),5)

    cv2.imwrite("RESULT.png",resultImg)

    return 

def FindShapes(ip):
    imgPath = ip
    img = cv2.imread(imgPath,0)
    imgCopy = cv2.imread(imgPath)
    height, width = img.shape


    ret, th = filter_image(img)

    cv2.imwrite('RESULT_0.png',th)

    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print "Contours: ",contours
    
    #print "len(contours): ",len(contours)

    hist_c,contours_array = get_histogram_contours(contours)
    
    t = basic_global_thresholding(hist_c)
    #print "t_hist: ",t
    contourBoxes = discard_contours(hist_c,contours_array,t)
    contourBoxes.pop(0) #delete the box of the background
    #print "contour boxes: ",contourBoxes

    draw_bounding_boxes(imgCopy,contourBoxes,15)

    cv2.imwrite('RESULT.png',imgCopy)

    return contourBoxes

#main()



    
            
            
