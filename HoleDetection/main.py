import cv2
from EdgeDetection import EdgeDetection as ed

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

    cv2.imwrite("verticalPeaks.png",originalImg)
    
main()

