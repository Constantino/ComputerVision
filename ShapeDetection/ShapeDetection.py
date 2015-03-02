from EdgeDetection import EdgeDetection as ed
class ShapeDetection:

	def __init__(self):
		
		self.myBackground = 0
		self.test = ed.EdgeDetection()

		if self.test.debug:
		    print "-> preprocessing the image"

    		self.test.path = ""

	def getNeighborhood(self,pixel):

	    neighborhood = []

	    for i in range(pixel[0]-1,pixel[0]+2):
		for j in range(pixel[1]-1,pixel[1]+2):
		    if i < self.test.height and j < self.test.width and i > 0 and j > 0:

		        neighborhood.append([i,j])

	    return neighborhood

	def isColor(self,pixel,color):

	    print "pixel: ",pixel
	    print "color: ",color
	    pixelColor = str(pixel[0])+str(pixel[1])+str(pixel[2])

	    return pixelColor == color

	def getBackground(self):

	    colors = {}
	    myBackground = {'color': 0, 'frecuency':0}

	    for r in range(self.test.height-1):
		for c in range(self.test.width-1):
		    pixelColor = str(self.test.originalImg[r,c][0])+str(self.test.originalImg[r,c][1])+str(self.test.originalImg[r,c][2])

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

	    return myBackground['color']

	def detectFigures(self):

            self.test.detectBorders()

            self.myBackground = self.getBackground()

	    figures = []
	    
	    while self.test.border:
		detected = self.applyDFS(self.test,self.test.border,self.myBackground)
		figures.append(detected)
		
		for i in detected:
		    self.test.imgCopy[i[0],i[1]] = 100
		    if [i[0],i[1]] in self.test.border:
		        self.test.border.remove([i[0],i[1]])
		
	    return figures

	def applyDFS(self,test,borders,myBackground):
	    visited = []
	    stack = []
	    point = []
	    
	    point = borders[0]
	    
	    visited.append(point)
	    stack.append(point)

	    while stack:

		neighborhood = self.getNeighborhood(point)

		connexions = []
		for e in neighborhood:

		    if e in borders or not self.isColor(test.originalImg[e[0],e[1]], str(myBackground)):
		        if e not in visited:
		            connexions.append(e)
		        
		            
		if not connexions:
		    point = stack.pop()
		else:
		    point = max(connexions)
		    visited.append(point)
		    stack.append(point)
	    
	    return visited


	def paintBorder(self):
	    for r in range(1,self.test.height-1,1):
		for c in range(1,self.test.width-1,1):
			if [r,c] in self.test.border:
				self.test.imgCopy[r,c] = 255
			else:
				self.test.imgCopy[r,c] = 0

	def drawBoundingBox(self,figures):	    
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

		color = [0,255,0]

		for z in range(x_min,x_max+1):
		    self.test.originalImg[y_min,z] = color
		    self.test.originalImg[y_max,z] = color
		for z in range(y_min,y_max+1):
		    self.test.originalImg[z,x_min] = color
		    self.test.originalImg[z,x_max] = color

		centerOfMass = [sum_y/n_elem,sum_x/n_elem]

		self.test.originalImg[centerOfMass[0],centerOfMass[1]] = [0,0,255]
