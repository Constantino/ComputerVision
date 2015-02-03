import cv2

debug = 0

#imagePath = "img/figures.png"
imagePath = "img/woman.jpeg"


img = cv2.imread(imagePath)
imgCopy = cv2.imread(imagePath)

height, width, depth = img.shape

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

def applyMasks(pixel):

    maskBuffer = []
    indexer = [-pixel[0]+1,-pixel[1]+1]
    for i in range(len(mask)):
        maskSum = 0
        for r in range(pixel[0]-1, pixel[0]+2):
            for c in range(pixel[1]-1,pixel[1]+2):
                maskSum += ((int(img[r,c][0])+int(img[r,c][1])+int(img[r,c][2]))/3)*mask[i][r+indexer[0]][c+indexer[1]]
        
        maskBuffer.append(maskSum)
        if debug:
            print "ms: ", maskSum

    maxMasks = max(maskBuffer)
    
    if debug:
        print "** Return max: ", maxMasks

    return maxMasks


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

def main():
    for y in range(1,height-1,1):
        for x in range(1,width-1,1):
            histogram.append( applyMasks([y,x]) )

    T = getThreshold(histogram)
    print "Threshold: ", T

    index_counter = 0
    for r in range(1,height-1,1):
        for c in range(1,width-1,1):
    
            print "h[",index_counter,"]: ",histogram[r+c]," > T: ",T
            if histogram[index_counter] > T:
                print "gonna print"
                imgCopy[r,c] = [255,255,255]
            else:
                imgCopy[r,c] = [0,0,0]

            index_counter += 1

    #for i in range(30,90):
    #    imgCopy[50,i] = [0,0,255]

    #print histogram

    cv2.imwrite("img/result.jpg",imgCopy)


main()
