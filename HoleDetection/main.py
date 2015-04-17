import cv2
from EdgeDetection import EdgeDetection as ed
from random import choice,randint

def preProcessImg(imagePath):
    originalImg = cv2.imread(imagePath)
    img = cv2.cvtColor(originalImg,cv2.COLOR_RGB2GRAY) #convert to grayscale                                                  
    imgCopy = img
    height, width = img.shape

    return originalImg,img,imgCopy,height,width

def getBorders(path):
    test = ed.EdgeDetection()

    test.path = path

    test.detectBorders()

    return paintBorder(test)

def paintBorder(test):

    for r in range(1,test.height-1,1):
        for c in range(1,test.width-1,1):
            if [r,c] in test.border:
                test.imgCopy[r,c] = 0
            else:
                test.imgCopy[r,c] = 255
    return test.imgCopy

def getHorizontalHistogram(height,width,imgCopy):
    hist = {}
    for c in range(1,width-1,1):
        sum_hist = 0
        for r in range(1,height-1,1):
            sum_hist += imgCopy[r,c]

        hist[c] = sum_hist

    return hist

def getVerticalHistogram(height,width,imgCopy):
    hist = {}
    for r in range(1,height-1,1):
        sum_hist=0
        for c in range(1,width-1,1):
            sum_hist += imgCopy[r,c]
        hist[r] = sum_hist

    return hist

def getPeaksByMean(histogram):
    peaks = {}
    sum_hist = 0

    for e in histogram:
        sum_hist += histogram[e]
    mean = sum_hist/len(histogram)
    
    for e in histogram:
        if histogram[e] < mean:
            peaks[e] = histogram[e]

    return peaks

def getBackground(originalImg,height,width):

    colors = {}
    myBackground = {'color': 0, 'frequency':0}
    
    for r in range(height-1):
        for c in range(width-1):
            pixelColor = originalImg[r,c][0]+ (originalImg[r,c][1])+ originalImg[r,c][2]

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

    print "colors: ",colors
    return [myBackground['color'],myBackground['frequency']],colors

def getFreqAverage(colors):
    sum_c = 0
    for e in colors:
        sum_c += colors[e]

    average = sum_c/len(colors)*1.0
    print "average: ",average
    return average

def paintBackground(originalImg,imgCopy,background,height,width):
    for r in xrange(height):
        for c in xrange(width):
            px_color = originalImg[r,c][0] + originalImg[r,c][1] + originalImg[r,c][2]
            Dif = abs(px_color - background[0])
            #print "Dif: ",Dif
            if px_color > 10: 
                
                imgCopy[r,c] = 255
    return imgCopy

def getNeighborhood(pixel,height,width):

    neighborhood = []

    for i in range(pixel[0]-1,pixel[0]+2):
        for j in range(pixel[1]-1,pixel[1]+2):
            if i < height and j < width and i > 0 and j > 0:
                
                neighborhood.append([i,j])
                
    return neighborhood


def applyDFS(img,start,validation,height, width):
    visited = []
    stack = []
    point = []
    
    point = start
    
    visited.append(point)
    stack.append(point)
    
    while stack:

        neighborhood = getNeighborhood(point,height,width)

        connexions = []
        for e in neighborhood:
            #print "Color img:", img[e[0],e[1]], "against val: ",validation
            if e in validation:
                if e not in visited:
                    connexions.append(e)

        if not connexions:
            point = stack.pop()
        else:
            point = max(connexions)
            visited.append(point)
            stack.append(point)

    return visited

def drawBoundingBox(figures,originalImg):    
    print "Drawing bounding-box"
    for i in figures:
                
        i.sort()
        n_elem = len(i)
        y_min = i[0][0]
        y_max = i[n_elem-1][0]
        x_min =  i[n_elem-1][1]
        x_max = 0

        sum_x = 0
        sum_y = 0

        for e in i:
            sum_x += e[1]
            sum_y += e[0]

            if e[1] > x_max:
                x_max = e[1]
            if e[1] < x_min:
                x_min = e[1]

            color = [randint(100,255),randint(100,255),randint(100,255)]

            for z in range(x_min,x_max+1):
                originalImg[y_min,z] = color
                originalImg[y_max,z] = color
            for z in range(y_min,y_max+1):
                originalImg[z,x_min] = color
                originalImg[z,x_max] = color

            centerOfMass = [sum_y/n_elem,sum_x/n_elem]

            originalImg[centerOfMass[0],centerOfMass[1]] = [0,0,255]

    return originalImg


def main():
    originalImg = None
    img = None
    imgCopy = None
    height = 0
    width = 0

    ColorHist = {}
    path = "HoleDetection/img/bulletHoles.jpg"

    originalImg, img, imgCopy, height, width = preProcessImg(path)
    background,colors = getBackground(originalImg,height,width)
    print "Background: ",background
    imgCopy = getBorders(path)

    cv2.imwrite("imgCopy.png",imgCopy)

    verticalHist = getVerticalHistogram(height,width,imgCopy)
    horizontalHist = getHorizontalHistogram(height,width,imgCopy)

    print "vHist: ",verticalHist
    print "hHist: ",horizontalHist

    verticalPeaks = getPeaksByMean(verticalHist)
    horizontalPeaks = getPeaksByMean(horizontalHist)

    red = [0,0,255]
    blue = [255,0,0]
    green = [0,255,0]

    for e in verticalPeaks:
        for c in xrange(width):
            originalImg[e,c] = green

    for e in horizontalPeaks:
        for r in xrange(height):
            originalImg[r,e] = blue

    holePeaks = []
    
    for v in verticalPeaks:
        for h in horizontalPeaks:
            if imgCopy[v,h] == 0:
                holePeaks.append([v,h])
                originalImg[v,h] = [0,0,255]

    holes = []
    while holePeaks != []:
        start = choice(holePeaks)
        visited = applyDFS(imgCopy,start,holePeaks,height, width)
        holes.append(visited)
        for e in visited:
            holePeaks.remove(e)


    
    for e in holes:
        color = [randint(100,255),randint(100,255),randint(100,255)]
        for px in e:
            originalImg[px[0],px[1]] = color

    
    originalImg = drawBoundingBox(holes,originalImg)

    cv2.imwrite("Peaks.png",originalImg)
    
main()

