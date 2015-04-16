import cv2

def preProcessImg(imagePath):
    originalImg = cv2.imread(imagePath)
    img = cv2.cvtColor(originalImg,cv2.COLOR_RGB2GRAY) #convert to grayscale                                                  
    imgCopy = img
    height, width = img.shape

    return originalImg,img,imgCopy,height,width

def getHorizontalHistogram(height,width,img):
    hist = {}
    for c in range(1,width-1,1):
        sum_hist = 0
        for r in range(1,height-1,1):
            sum_hist += img[r,c]

        hist[c] = sum_hist

    return hist

def getVerticalHistogram(height,width,img):
    hist = {}
    for r in range(1,height-1,1):
        sum_hist=0
        for c in range(1,width-1,1):
            sum_hist += img[r,c]
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
            if Dif < 150: 
                
                imgCopy[r,c] = 255

    cv2.imwrite("imgCopy.png",imgCopy)

def main():
    originalImg = None
    img = None
    imgCopy = None
    height = 0
    width = 0

    ColorHist = {}

    originalImg, img, imgCopy, height, width = preProcessImg("img/holes_test2.jpg")
    background,colors = getBackground(originalImg,height,width)
    print "Background: ",background
    paintBackground(originalImg,imgCopy,background,height,width)

    verticalHist = getVerticalHistogram(height,width,img)
    horizontalHist = getHorizontalHistogram(height,width,img)

    print "vHist: ",verticalHist
    print "hHist: ",horizontalHist

    verticalPeaks = getPeaksByMean(verticalHist)
    horizontalPeaks = getPeaksByMean(horizontalHist)

    red = [0,0,255]
    blue = [255,0,0]

    for e in verticalPeaks:
        for c in xrange(width):
            originalImg[e,c] = red

    for e in horizontalPeaks:
        for r in xrange(height):
            originalImg[r,e] = blue

    cv2.imwrite("verticalPeaks.png",originalImg)
    
main()


