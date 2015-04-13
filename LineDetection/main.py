import cv2
from Tkinter import *
from tkFileDialog import *
import sys
from numpy import *
#from EdgeDetection import EdgeDetection as ed
from ShapeDetection import ShapeDetection as sd
import math
from random import randint
from PIL import Image, ImageTk

def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
    return incluidos

#starting
shapeDetector = sd.ShapeDetection()
shapeDetector.test.path = 'LineDetection/'+'basicFigures.jpg'
shapeDetector.test.detectBorders()
background = shapeDetector.getBackground()
imagen = shapeDetector.test.originalImg


incluir = 1.0
CERO = 0.00001
resultado = list()
index_counter = 0
w=shapeDetector.test.width
h=shapeDetector.test.height
for y in xrange(1,h-1,1):
	datos = list()
	for x in xrange(1,w-1,1):
            """
            pixel_X = float(sum(imagen_X[x, y]))/3.0
            pixel_Y = float(sum(imagen_Y[x, y]))/3.0
            print str(pixel_X) + " " + str(pixel_Y)
            if fabs(pixel_X) > CERO:
            angulo = atan(pixel_Y/pixel_X)
            else:
            if fabs(pixel_X) + fabs(pixel_Y) <= CERO:
            angulo = None
            elif pixel_X == 0.0 and pixel_Y == 255.0:
            angulo = 90.0
            else:
            angulo = 0.0
            """
            #angulo = shapeDetector.test.angles[index_counter]
            if [y,x] in shapeDetector.test.border:
                
                angulo = shapeDetector.test.borderInfo[index_counter][2]
                anguloGrados = angulo*180/math.pi
                #imagen[y,x] = [255,0,255]  
                print "angulo -> ",angulo," grados: ",anguloGrados
                angulo = anguloGrados
                if angulo is not None:
                    rho = (x - w/2) * cos(angulo) + (h/2 - y) * sin(angulo)
                    datos.append(('%d' % angulo, '%d' % rho))
                else:
                    datos.append((None, None))

                index_counter += 1

            else:
                datos.append((None,None))
                
        resultado.append(datos)
		

comb = dict()
for y in xrange(1,len(resultado),1):
	for x in xrange(1,len(resultado[y]),1):
		if x > 0 and y > 0 and x < w - 1 and y < h - 1:
			print "-> y,x: ",y,",",x
			(angulo, rho) = resultado[y][x]
			if angulo is not None:
			    combinacion = (angulo, rho)
			    if combinacion in comb:
				comb[combinacion] += 1
			    else:
				comb[combinacion] = 1

frec = frecuentes(comb, int(ceil(len(comb) * incluir)))
"""
def getAverages(t,hist):

            sum_upper = 0
            counter_upper = 0

            sum_down = 0
            counter_down = 0
            for e in hist:
                if e > t: #sum all the gradients > threshold                                                                                    
                    sum_upper += e
                    counter_upper += 1
                else: #sum all the gradients < threshold                                                                                        
                    sum_down += e
                    counter_down += 1

            return [(sum_upper/counter_upper*1.0),(sum_down/counter_down*1.0)] #return means   

hist = []
for e in comb:
    hist.append(comb[e])


t_new = max(hist)/2.0 #the threshold should be close to the center                                                             
t_old = 0.0
mean = [0,0]
t = 0
while abs(t_old-t_new) > 0.001: #the loop ends until the difference of the old threshold and the new one is minimum                 
    
    mean = getAverages(t_new,hist) #get the average of each side based on the current threshold                                     
    t_old = t_new
    t_new = 0.5*(mean[0]+mean[1]) # get a new threshold by obtaining the average of the means                                       
    
    t = t_new/2.5


"""
#print "Comb: ", comb
frec = []

for i in comb:
    if comb[i] > 1:#t:
            
        frec.append(i)

print "frec: ",frec

print "Comb: ", comb

#drawLines
def drawLines(rho, angle,h,w):
    a = float(angle)
    rho = float(rho)
    for x in range(1,w-1,1):
        y_n = ( rho - x*math.cos(a) ) / math.sin(a)
        if y_n < h and y_n > 0:
            imagen[y_n,x] = [0,0,255]

for y in xrange(1,len(resultado)-1,1):
	renglon = list()
	for x in xrange(1,len(resultado[y])-1,1):
		(ang, rho) = resultado[y][x]
                #print "angulo: ", ang
                
		if (ang, rho) in frec:
                    imagen[y,x] = [0,255,0]
                    #drawLines(rho,ang,h,w)
                    ang = abs(float(ang))
                    if ( ang < 100 and ang > 80 ):
                        #imagen.putpixel((x,y), (0,255,0))
                        imagen[y,x] = [0,255,0]
                    elif ang > 0 and ang < 25:
                        #imagen.putpixel((x,y), (0,0,255))
                        imagen[y,x] = [0,0,255]
                        #dummy = 1
                    elif ang < 80 and ang > 25:
                        imagen[y,x] = [255,100,255]
                    elif ang > 100 and ang < 135:
                        imagen[y,x] = [100,100,255] 
                    elif ang > 135 and ang < 155: 
                        imagen[y,x] = [100,100,100] 
                    else:
                        #imagen.putpixel((x,y), (255,0,0))
                        imagen[y,x] = [255,0,0]
                        #d = 1
                    
                

#for y in xrange

cv2.imwrite("myFuckingLines.png",imagen)
#imagen.save("Prueba.jpg")
#return imagen

