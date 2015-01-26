import cv2

colors = {}
myBackground = {'color':0,'frequency':0}

def findColors():
    #print "Findcolors "
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

    return


def isColor(pixel,color):
    pixelColor = str(pixel[0])+str(pixel[1])+str(pixel[2])
    return pixelColor == color


def getNeighbors(position):
    
    neighbors = []
    for i in range(position[0]-1,position[0]+2):
        for j in range(position[1]-1, position[1]+2):
            if [i,j] != [position[0],position[1]] and i < height and j < width:
                neighbors.append([i,j])

    neighbors.sort()

    return neighbors


coordinates = []
def findForm():
    print "findForm"
    for i in range(height):
        for j in range(width):
            if not isColor(img[i,j],myBackground['color']):
               img[i,j] = [0,255,0]
               coordinates.append([i,j])
               
    return


border = []
def paintBorder():
    for c in coordinates:
        neighborhood =  getNeighbors(c)
        hasBackground = 0
        hasGreen = 0
        for n in neighborhood:
            if isColor(img[n[0],n[1]],myBackground['color']):
                hasBackground += 1
            if isColor(img[n[0],n[1]],"02550"):
                hasGreen += 1
        if hasBackground > 0 and hasGreen > 2:
            img[c[0],c[1]] = [0,0,0]
            border.append(c)

def pointX():
    for c in coordinates:
        neighborhood = getNeighbors(c)
        counter = 0
        for n in neighborhood:
            #print n
            if isColor(img[n[0],n[1]],"02550"):
                counter += 1
        if counter == 8:
            return c

def pointX2(p1,p2): #still for testing
    for c in coordinates:
        if not (c > [28,43] and c < [59,78]):
            
            neighborhood = getNeighbors(c)
            counter = 0
            for n in neighborhood:
                #print n
                if isColor(img[n[0],n[1]],"02550"):
                    counter += 1
            if counter == 8:
                img[c[0],c[1]] = [255,0,0]
                return c


myObject = []
def findingObject():
    start = []
    nextOne = []
    caught = 0
    
    old_len = 0

    while caught <= 2:

        if nextOne:
            neighborhood = getNeighbors(nextOne)
            if caught > 1:
                print "nextOne: ",nextOne,"  neighborhood: ",neighborhood
        else:
            pX = pointX()
            neighborhood = getNeighbors([pX[0]-1,pX[1]-1])

        hasBlack = 0
        hasGreen = 0

        old_len = len(myObject)

        for n in neighborhood:
            if n in border and n not in myObject:
                img[n[0],n[1]] = [0,0,255]
                myObject.append(n)

        #if old len of myObject is equal to the current one, so it's caught in the loop
        if old_len == len(myObject): 
            print "caught"
            caught += 1 
            l = len(myObject)
            nextOne = myObject[l-caught]

        else:
            l = len(myObject)
            nextOne = myObject[l-1]

        print myObject        
        print "len_myObject: ", len(myObject)," len_border: ", len(border)



point1 = []
point2 = []
def drawBox():

    myObject.sort()
    length = len(myObject)

    print "myObject: ", myObject

    xMin, yMin = myObject[0]
    xMax, yMax = myObject[length-1]

    print "xMin: ",xMin," yMin:",yMin," xMax:",xMax," yMax:",yMax

    point1 = [xMin,yMin]
    point2 = [xMax,yMax]

    for e in myObject:
        if e[1] < yMin:
            yMin = e[1]
        if e[1] > yMax:
            yMax = e[1]

        if e[0] < xMin:
            xMin = e[0]
        if e[0] > xMax:
            xMax = e[0]
        
    for x in range(xMin,xMax,1):
        img2[x,yMin] = [0,0,255]
        img2[x,yMax] = [0,0,255]
    for y in range(yMin,yMax,1):
        img2[xMin,y] = [0,0,255]
        img2[xMax,y] = [0,0,255]


#Image properties
path = "pictures/"
filename = "circle.jpg"

img = cv2.imread(path+filename) #picture as a buffer
img2 = cv2.imread(path+filename) #final picture
height, width, depth = img.shape

def main():
    findColors()
    findForm()
    paintBorder()
    findingObject()

    drawBox()

    #findingObject()

    cv2.imwrite(path+"result.jpg",img2)
    #cv2.imshow('image',img)
    cv2.imshow('image',img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
