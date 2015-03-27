from random import randint, random
from math import sqrt, ceil, floor, fabs, atan2, cos, sin, pi
import numpy as np
import cv2
from ShapeDetection import ShapeDetection as sd

def getTangentEq(test):
    point1,gradient1,angle1 = test.borderInfo[0]
    point2, gradient2, angle2 = test.borderInfo[110]

    eq1 = processTangent(point1,angle1,test)
    eq2 = processTangent(point2,angle2,test)
    print "eq1: ",eq1
    print "eq2: ",eq2
    y,x = getLinearEq(eq1,eq2,test)
    print "y,x: ",y,",",x
    
    if y != 0 and x != 0:

        if y > 0 and y < test.height and x > 0 and x < test.width:
            for r in range(y-1,y+2,1):
                for c in range(x-1,x+2,1):
                    test.originalImg[r,c] = [0,0,255]

    drawLineBetweenPoints(point1,point2,test)
    
    cv2.imwrite("Tangents_ellipse.png",test.originalImg)

    return 

def processTangent(point,angle,test):

    angle = 3.1416/2-angle

    dx = cos(angle)
    dy = sin(angle)
 
    m = dx/dy
    
    secondPoint = [int(round(m*(100-point[1])+point[0])), 100]

    for c in xrange(test.width):
        y = int(round(m*(c-point[1])+point[0]))
        #print "y: ",y                                                                                                                      
        if y >= 0 and y < test.height:
            test.originalImg[y,c] = [0,255,0]

    cv2.imwrite("Tangents_"+str(m)+".png",test.originalImg)

    eq = [m,point,secondPoint[0]]
    

    return eq

def getLinearEq(eq1,eq2,test):

    y1, y2 = int(), int()

    for x in xrange(-test.width*6,test.width*6,1):
        y1 = int(round(eq1[0]*(x-eq1[1][1])+eq1[1][0]))
        y2 = int(round(eq2[0]*(x-eq2[1][1])+eq2[1][0]))
        if y1 == y2:
            print "y1 == y2 = ",y1
            return y1,x
    
    return 0,0

def drawLineBetweenPoints(point1, point2,test):
    print "part1: ",(point2[0]-point1[0])
    print "part2: ",(point2[1]-point1[1])
    m = (point2[0]-point1[0])*1.0/(point2[1]-point1[1])
    print "**m ",m

    b = min(point2[0],point1[0])

    start = min(point1[1],point2[1])
    finish = max(point1[1],point2[1])

    print "p1, p2: ",point1," , ",point2

    for x in range(start,finish,1):
        y = int( round( m*(x - start) + b ) )
        print "-.--> y: ",y," m: ",m," b: ",b
        if y > 0  and y < test.height:
            test.originalImg[y,x] = [255,0,0]

    cv2.imwrite("Tangents_"+str(m)+".png",test.originalImg)

    return 

def getAllTangents(test):

    for item in range(0,len(test.borderInfo)-1,1):
        point,gradient,angle = test.borderInfo[item]#test.borderInfo[300]

        print "Point1: ", point

        #test.originalImg[point[0],point[1]] = [255,0,0] #Paint point 1
    
        print "-> Gradient: ",gradient
        print "-> Angle: ",angle

        angle = 3.1416/2-angle
        
        print "angle: ", angle
        dx = cos(angle)
        dy = sin(angle)

        #m = dy/dx
        m = dx/dy
        print "dx,dy: ",dx,",",dy
        print "m: ",m

        
        #for r in xrange(test.height):
        for c in xrange(test.width):
            y = int(round(m*(c-point[1])+point[0]))
            #print "y: ",y
            if y >= 0 and y < test.height:
                test.originalImg[y,c] = [0,255,0]

                
        cv2.imwrite("Tangents_ellipse.png",test.originalImg)

    return

def testPaintBorders(height,width,test):
    print "-> Painting borders"
    
    for l in test.borderInfo:
        
        coord = l[0]
        if coord[0] < height and coord[1] < width:
            test.originalImg[coord[0],coord[1]] = [0,0,255]
        
            
    cv2.imwrite("Borders_ellipse.png",test.originalImg)


def main():
    
    shapeDetector = sd.ShapeDetection()

    shapeDetector.test.path = "img/ellipse.png"

    #figures = shapeDetector.detectFigures()
    shapeDetector.test.detectBorders()

    width = shapeDetector.test.width
    height = shapeDetector.test.height

    #testPaintBorders(height,width, shapeDetector.test)
    #getAllTangents(shapeDetector.test)
    getTangentEq(shapeDetector.test)
    

main()

