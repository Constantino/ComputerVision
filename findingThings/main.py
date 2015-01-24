import cv2
import numpy as np

colors = {}
myBackground = {'color':0,'frequency':0}

def findColors(width, height, img):
    
    for i in range(height):
        for j in range(width):

            pixelColor = str(img[i,j][0])+str(img[i,j][1])+str(img[i,j][2])

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

    
    #print myBackground
    return

def findForm(width,height,img):
    for i in range(height):
        for j in range(width):
            pixelColor = str(img[i,j][0])+str(img[i,j][1])+str(img[i,j][2])
            if pixelColor != myBackground['color']:
               img[i,j] = [0,255,0]
    return

def drawBox():
    
    return


img = cv2.imread("../circle.jpg")
height, width, depth = img.shape

findColors(width,height,img)
findForm(width,height,img)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
