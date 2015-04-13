import cv2
from numpy import *
from ShapeDetection import ShapeDetection as sd
import math
from random import randint

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
shapeDetector.test.path = 'LineDetection/'+'train.jpg'
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
            #angulo = shapeDetector.test.angles[index_counter]
            if [y,x] in shapeDetector.test.border:
                
                angulo = shapeDetector.test.borderInfo[index_counter][2]
                anguloGrados = angulo*180/math.pi
                
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
frec = []

for i in comb:
    if comb[i] > 1:#t:
            
        frec.append(i)

print "frec: ",frec

print "Comb: ", comb

for y in xrange(1,len(resultado)-1,1):
	renglon = list()
	for x in xrange(1,len(resultado[y])-1,1):
		(ang, rho) = resultado[y][x]
            
		if (ang, rho) in frec:
                    imagen[y,x] = [0,255,0]
                    
                    ang = abs(float(ang))
                    if ( ang < 100 and ang > 80 ):
                        
                        imagen[y,x] = [0,255,0]
                    elif ang > 0 and ang < 25:
                    
                        imagen[y,x] = [0,0,255]
                        
                    elif ang < 80 and ang > 25:
                        imagen[y,x] = [255,100,255]
                    elif ang > 100 and ang < 135:
                        imagen[y,x] = [100,100,255] 
                    elif ang > 135 and ang < 155: 
                        imagen[y,x] = [100,100,100] 
                    else:
                        
                        imagen[y,x] = [255,0,0]
                        
                    
cv2.imwrite("Output_Lines.png",imagen)

