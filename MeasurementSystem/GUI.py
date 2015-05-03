import sys,pygame

pygame.init()

image = pygame.image.load("test/test017.jpg")

image = pygame.transform.scale(image,(400,600))

imagerect = image.get_rect()
width, height = imagerect.size

size = ((width+150),height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Measurement System")
font = pygame.font.Font(None, 20)
btnFindObjects = font.render('Find Shapes',1,(0,0,250)) 
btnSelectReference = font.render('Select reference',1,(0,255,0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            cordx, cordy  = pygame.mouse.get_pos() 
            if 0 < cordx < 100 and 0 < cordy < 25:
                print "btnFindObjects"
            if 0 < cordx < 100 and 35 < cordy < 55:
                print "btnSelectReference"
    
    screen.fill((0,0,0))
    screen.blit(image,(150,0))
    screen.blit(btnFindObjects,(0,10))
    screen.blit(btnSelectReference,(0,40))
    
    pygame.display.flip()
