import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *

class FormDetection:

    def getNeighborhood(self,pixel):
        
        neighborhood = []

        for i in range(pixel[0]-1,pixel[0]+2):
            for j in range(pixel[1]-1,pixel[1]+2):
                
                neighborhood.append([i,j])
        
        return neighborhood
        

    def applyDFS(self):
        visited = []
        stack = []

        point = self.border[0]

        visited.append(point)
        stack.append(point)

        while stack:

            neighborhood = self.getNeighborhood(point)

            connexions = []
            for e in neighborhood:
                if e in self.border:
                    if e not in visited:
                        connexions.append(e)
            
            if not connexions:
                point = stack.pop()
            else:
                point = max(connexions)
                visited.append(point)
                stack.append(point)

        
        
        
