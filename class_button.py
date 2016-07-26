from class_figure import *
from class_block import *

####################################
# Button Class
####################################

class MyButton(object):

	def __init__(self,x,y,w,h,c,t):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.color = c
		self.type = t

	def wasClicked(self,x,y):
		return ((self.x <= x <= self.x + self.width) and
				(self.y <= y <= self.y + self.height))

	def __repr__(self):
		return "button type: " + str(self.type)

	def draw(self,canvas,codeWidth=0,vertical=True):
		x1 = self.x
		y1 = self.y
		x2 = x1 + self.width
		y2 = y1 + self.height
		if vertical: canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
		elif x1<codeWidth:
			if x2 > codeWidth: x2 = codeWidth
			canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)

####################################
# Figure Button Class
####################################

class FigureButton(MyButton):

	def __init__(self,w,h,c,t):
		self.x = 0
		self.y = 0
		self.width = w
		self.height = h
		self.color = c
		self.type = t

	def createfigure(self,figures,propertyBoxBounds):
		x1,y1 = self.x, self.y
		w,h = self.width, self.height
		figure = Figure(x1,y1,w,h,self.color,self.type,propertyBoxBounds)
		figure.name += str(len(figures))
		figures.append(figure)

####################################
# Block Button Class
####################################

#from class_block import *

class BlockButton(MyButton):

	def __init__(self,x,y,w,h,c,t):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.color = c
		self.type = t

	def createBlock(self,data):
		x1,y1 = self.x, self.y
		w,h = self.width, self.height
		if self.type == "move": block = MoveBlock(x1,y1,data.figures)
		elif self.type == "loop": block = LoopBlock(x1,y1)
		else: block = Block(x1,y1,w,h,self.color,self.type)
		data.blocks.append(block)


bb = BlockButton(0,0,10,10,"blue","block")
b = MyButton(0,0,10,10,"green","regular")
fb = FigureButton(10,10,"yellow","figure")
print(bb)

# from class_block import Block
# block = Block(10,10,10,10,"blue","block")