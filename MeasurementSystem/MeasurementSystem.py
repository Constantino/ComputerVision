import cv2
import numpy as np
from matplotlib import pyplot as plt
from random import choice,randint
import math

imgPath = "test/test004.jpg"
img = cv2.imread(imgPath,0)
imgCopy = cv2.imread(imgPath)

def filter_image(img):
    # Otsu's thresholding after Gaussian filtering                                                                                             
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return ret,th
    
def get_contours(th):
    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def main():
    ret, th = filter_image(img)
    contours = get_contours(th)

    print "len(contours): ",len(contours)

main()

    
            
            
