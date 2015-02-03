import cv2

debug = 1

imagePath = "img/figures.png"

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


def main():
    for y in range(50,70,1):
        for x in range(50,70,1):
            histogram.append( applyMasks([y,x]) )


main()
