import cv2
from Tkinter import *
from tkFileDialog import *

debug = 0

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
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    imgCopy = img
    height, width = img.shape

    return img,imgCopy,height,width

def loadFile():
    fname = ""
    try:
        fname = askopenfilename(filetypes=(("JPG", "*.jpg"),
        ("All files", "*.*")))

    except ValueError:
        print "Please select an image. Try again..."

    return fname

def applyMasks(pixel,img):

    pixelGradients = []
    indexer = [-pixel[0]+1,-pixel[1]+1]

    for i in range(len(mask)):
        gradient = 0
        for r in range(pixel[0]-1, pixel[0]+2):
            for c in range(pixel[1]-1,pixel[1]+2):
                gradient += img[r,c]*mask[i][r+indexer[0]][c+indexer[1]]
        
        pixelGradients.append(gradient)

        if debug:
            print "-> gradient: ", gradient

    maxGradient = max(pixelGradients)
    
    if debug:
        print "-> Return max: ", maxGradient

    return maxGradient


def getThreshold(histogram):

    t_new = max(histogram)/2.0
    t_old = 0.0
    mean = [0,0]
    while abs(t_old-t_new) > 0.001:

        print "t_new: ",t_new

        mean = getAverages(t_new)
        t_old = t_new
        t_new = 0.5*(mean[0]+mean[1])
        
    print "returning value"
    return t_new

def getAverages(t):
    
    sum_upper = 0
    counter_upper = 0

    sum_down = 0
    counter_down = 0
    for e in histogram:
        if e > t:
            sum_upper += e
            counter_upper += 1
        else:
            sum_down += e
            counter_down += 1

    return [(sum_upper/counter_upper*1.0),(sum_down/counter_down*1.0)]

def processImage():

    path = loadFile()

    if path == "":

        if debug:
            print "loadFile: --"

        return

    if debug:
        print "loadfile: ", fileImg
        
    img,imgCopy,height,width = preProcessImg(path)

    for y in range(1,height-1,1):
        for x in range(1,width-1,1):
            histogram.append( applyMasks([y,x],img) )

    T = getThreshold(histogram)
    
    if debug:
        print "-> Threshold: ", T

    index_counter = 0
    for r in range(1,height-1,1):
        for c in range(1,width-1,1):

            if debug:
                print "h[",index_counter,"]: ",histogram[r+c]," > T: ",T

            if histogram[index_counter] > T:
                
                imgCopy[r,c] = 255
            else:
                
                imgCopy[r,c] = 0

            index_counter += 1

    cv2.imwrite("img/result.png",imgCopy)


def main():
    master = Tk()

    f = Frame(master, height=300, width=300)
    f.pack_propagate(0)
    f.pack()

    b = Button(f, text="Load a picture", command = processImage)
    b.pack()

    mainloop()

main()
