import sys,pygame
from MeasurementSystem import *
from tkFileDialog import *

def loadFile():
    fname = ""
    try:
        fname = askopenfilename(filetypes=(("All files", "*.*"),
                                           ("PNG", "*.png")))

    except ValueError:
        print "Please select an image. Try again..."

    return fname

pygame.init()
imgPath = loadFile()
image = pygame.image.load(imgPath)

imagerect = image.get_rect()
realWidth, realHeight = imagerect.size

scaleWidth, scaleHeight = 400,600
image = pygame.transform.scale(image,(scaleWidth,scaleHeight))

imagerect = image.get_rect()
width, height = imagerect.size

panel = 90
topPanel = 40

size = ((width+panel),(height+topPanel))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Measurement System")
font = pygame.font.Font(None, 20)

btnFindObjects = font.render('Find Objects',1,(0,0,250)) 
btnMeasureCm = font.render('Measure (cm)',1,(0,255,0))
btnMeasureIn = font.render('Measure (in)',1,(0,255,0))
btnMeasureMm = font.render('Measure (mm)',1,(0,255,0))
btnMeasureline = font.render('Measure (line)',1,(0,255,0))

found = False
isReadyToMeasure = False
message = font.render('',1,(255,0,0))
isObject = False
objectIndex = int()
isWaiting2P = False

scaleW, scaleH = int(),int()

point1, point2 = (0,0)
counter = 0

global contourBoxes

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            cordx, cordy  = pygame.mouse.get_pos() 
            if 0 < cordx < panel and topPanel < cordy < 25+topPanel:
                print "btnFindObjects"
                print "Select an object as reference"
                message = font.render('Select an object as reference',1,(255,0,0))
                found = True
            
                contourBoxes = FindShapes(imgPath)

                image = pygame.image.load("RESULT.png")
                image = pygame.transform.scale(image,(400,600))


            if 0 < cordx < panel and (35+topPanel) < cordy < (55+topPanel): #measure in cm
                
                if found and isObject and objectIndex >= 0:
                    print "objectIndex: ",objectIndex
                    Measure(objectIndex,contourBoxes,"cm")

                    image = pygame.image.load("RESULT.png")
                    image = pygame.transform.scale(image,(scaleWidth,scaleHeight))
                    message = font.render("Measurement complete",1,(255,0,0))

                else:
                    print "Select an object"
                    message = font.render("Select an object",1,(255,0,0))

            if 0 < cordx < panel and (topPanel*3) < cordy < (topPanel*3+20): #measure in inches
                
                if found and isObject and objectIndex >= 0:
                    print "objectIndex: ",objectIndex
                    Measure(objectIndex,contourBoxes,"in")

                    image = pygame.image.load("RESULT.png")
                    image = pygame.transform.scale(image,(scaleWidth,scaleHeight))
                    message = font.render("Measurement complete",1,(255,0,0))

                else:
                    print "Select an object"
                    message = font.render("Select an object",1,(255,0,0))


            if 0 < cordx < panel and (topPanel*4) < cordy < (topPanel*4+20): #measure in mm
                
                if found and isObject and objectIndex >= 0:
                    print "objectIndex: ",objectIndex
                    Measure(objectIndex,contourBoxes,"mm")

                    image = pygame.image.load("RESULT.png")
                    image = pygame.transform.scale(image,(scaleWidth,scaleHeight))
                    message = font.render("Measurement complete",1,(255,0,0))

                else:
                    print "Select an object"
                    message = font.render("Select an object",1,(255,0,0))

            if 0 < cordx < panel and (topPanel*5) < cordy < (topPanel*5+20): #measure line
                
                if found and isObject and objectIndex >= 0:
                    print "objectIndex: ",objectIndex
                    #MeasureLine(objectIndex,line,"in")
                    """
                    image = pygame.image.load("RESULT.png")
                    image = pygame.transform.scale(image,(scaleWidth,scaleHeight))
                    """
                    message = font.render("Select 2 points",1,(255,0,0))
                    isWaiting2P = True
                        
                        
                else:
                    print "Select an object"
                    message = font.render("Select an object as reference",1,(255,0,0))
                
        
            if panel < cordx < (width+panel) and topPanel < cordy < (height+topPanel):
                if found and (not isWaiting2P):
                    print "Checking if it is an object"
                    
                    print "w and h ", width,realWidth,height,realHeight
                    scaleW = (realWidth*1.0)/width
                    scaleH = (realHeight*1.0)/height
                    #print "scales: ",scaleW,scaleH
                    isObject,objectIndex = getReferenceObject((cordx-panel,cordy-topPanel),contourBoxes,scaleW,scaleH)
                    msgString = ""

                    if isObject:
                        msgString = "Object selected"
                    else:
                        msgString = "Select an object as reference"
                    
                    message = font.render(msgString,1,(255,0,0))
    
                    image = pygame.image.load("RESULT.png")
                    image = pygame.transform.scale(image,(400,600))

                else:
                    if found:
                        if counter == 0:
                            point1 = (cordx,cordy)
                            counter += 1
                            DrawPoint((point1[0]-panel,point1[1]-topPanel),scaleW,scaleH)
                
                        elif counter == 1:
                            point2 = (cordx,cordy)
                            DrawPoint((point2[0]-panel,point2[1]-topPanel),scaleW,scaleH)
                            counter += 1

                        if counter == 2:
                            counter = 0
                            print "points: ",point1,point2
                            isWaiting2P = False

                        image = pygame.image.load("RESULT.png")
                        image = pygame.transform.scale(image,(scaleWidth,scaleHeight))

                    else:                        
                        print "You must find shapes first"
                        message = font.render('You must find shapes first',1,(255,0,0))                
    


    screen.fill((0,0,0))
    screen.blit(image,(panel,topPanel))
    screen.blit(message,(200,15))
    screen.blit(btnFindObjects,(0,topPanel))
    screen.blit(btnMeasureCm,(0,topPanel*2))
    screen.blit(btnMeasureIn,(0,topPanel*3))
    screen.blit(btnMeasureMm,(0,topPanel*4))
    screen.blit(btnMeasureIn,(0,topPanel*5))
    
    pygame.display.flip()
