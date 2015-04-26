import cv2
import numpy as np
from matplotlib import pyplot as plt
from random import choice,randint
import math

imgPath = "test004.jpg"
img = cv2.imread(imgPath,0)
imgCopy = cv2.imread(imgPath)

# Otsu's thresholding after Gaussian filtering                                                                                                  
blur = cv2.GaussianBlur(img,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

contours, hierarchy = cv2.findContours(th3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

print "len(contours): ",len(contours)
