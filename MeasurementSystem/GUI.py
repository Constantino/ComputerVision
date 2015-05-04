import sys,pygame
from MeasurementSystem import *

pygame.init()
imgPath = "test/test021.jpg"
image = pygame.image.load(imgPath)

imagerect = image.get_rect()
realWidth, realHeight = imagerect.size

image = pygame.transform.scale(image,(400,600))

imagerect = image.get_rect()
width, height = imagerect.size

panel = 90
topPanel = 40

size = ((width+panel),(height+topPanel))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Measurement System")
font = pygame.font.Font(None, 20)

btnFindObjects = font.render('Find Shapes',1,(0,0,250)) 
btnMeasure = font.render('Measure',1,(0,255,0))
found = False
message = font.render('',1,(255,0,0))

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


            if 0 < cordx < panel and (35+topPanel) < cordy < (55+topPanel):
                print "btnSelectReference"

            if panel < cordx < (width+panel) and topPanel < cordy < (height+topPanel):
                if found:
                    print "Checking if it is an object"
                    message = font.render('Checking if it is an object',1,(255,0,0))
                    print "w and h ", width,realWidth,height,realHeight
                    scaleW = (realWidth*1.0)/width
                    scaleH = (realHeight*1.0)/height
                    print "scales: ",scaleW,scaleH
                    getReferenceObject((cordx-panel,cordy-topPanel),contourBoxes,scaleW,scaleH)
                    
                    image = pygame.image.load("RESULT.png")
                    image = pygame.transform.scale(image,(400,600))

                else:
                    print "You must find shapes first"
                    message = font.render('You must find shapes first',1,(255,0,0))                
    


    screen.fill((0,0,0))
    screen.blit(image,(panel,topPanel))
    screen.blit(message,(200,15))
    screen.blit(btnFindObjects,(0,topPanel))
    screen.blit(btnMeasure,(0,topPanel*2))
    
    pygame.display.flip()
