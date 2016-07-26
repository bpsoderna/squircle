from class_figure import *
from class_block import *


####################################
# Figure Class
####################################

class Figure(object):

    def __init__(self,x,y,w,h,c,t,propertyBoxBounds):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.drag = False
        self.dx = 0
        self.dy = 0
        self.type = t
        self.propertyBoxBounds = propertyBoxBounds
        self.displayPropertyBox = False
        self.name = t

    #####################
    # Figure Methods
    #####################

    def __repr__(self):
        return self.name

    def __eq__(self,other):
        if type(other) == str:
            return other == self.name
        elif isinstance(other,Figure):
            return self.name == other.name
        else:
            return False

    def clicked(self,x,y):
    #returns True if the figure was clicked
        return (self.x < x < self.x + self.width and 
                self.y < y < self.y + self.height)

    def reset(self,trashcan,figures):
    #'unselects' figure and deletes it if it's in the trashcan
        self.drag = False
        if self.isInTrashcan(trashcan):
            figures.pop(figures.index(self))

    def isInBounds(self,canvasBounds): 
    #determines if the figure has left the canvas
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        w1, h1, w2, h2 = canvasBounds
        return x1>w1 and x2<w2 and y1>h1 and y2<h2

    def isInTrashcan(self,trashcan):
    #determines if the figure is in the trashcan
        w1, w2 = trashcan.x1, trashcan.x2
        h1, h2 = trashcan.y1, trashcan.y2
        x1, y1 = self.x, self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        return (((w1<x1<w2) and (h1<y1<h2)) or ((w1<x2<w2) and (h1<y2<h2)) or
                ((w1<x1<w2) and (h1<y2<h2)) or ((w1<x2<w2) and (h1<y1<h2)))

    #####################
    # Run Methods
    #####################

    def runMove(self,direction,pixles):
        if direction == "Up":
            self.y -= pixles
        elif direction == "Down":
            self.y += pixles
        elif direction == "Right":
            self.x += pixles
        elif direction == "Left":
            self.x -= pixles
        else:
            pass

    #####################
    # Figure Motion
    #####################

    def move(self,x,y,clickedfigure):
    #moves a clicked block
        if self.drag:
            self.x = x - self.dx
            self.y = y - self.dy
            clickedfigure = self
        return clickedfigure

    def selectIndividual(self,x,y):
    #selects one clicked block and displays its property box
        x1, y1 = self.x, self.y
        if self.clicked(x,y):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.displayPropertyBox = True
        else:
            #Note: if clicking on multiple boxes at once, displays both boxes
            self.displayPropertyBox = False

    def panScreen(self,event,canvasBounds,clickedFigure,newFigure): 
    #moves the figure on the canvas to simulate panning
        if not self.drag and clickedFigure != None and not newFigure:
            #note: does not pan when placing new blocks
            #note: can pan things into the trash
            x1, y1 = clickedFigure.x, clickedFigure.y
            x2, y2 = x1 + clickedFigure.width, y1 + clickedFigure.height
            w1, h1, w2, h2 = canvasBounds
            if   x1<w1: self.x += 1
            elif x2>w2: self.x -= 1
            if   y1<h1: self.y += 1
            elif y2>h2: self.y -= 1

    #####################
    # Figure Drawing
    #####################

    def draw(self,canvas,canvasBounds,trashcan):
        x1,y1,w,h = self.x, self.y, self.width, self.height
        c = self.color
        self.drawPropertyBox(canvas)
        if self.isInTrashcan(trashcan):
            c = "gray"
        if self.isInBounds(canvasBounds):
            canvas.create_rectangle(x1,y1,x1+w,y1+h,fill=c)
        else:
            self.drawPartialFigure(canvas,canvasBounds,c)

    def drawPartialFigure(self,canvas,canvasBounds,c):
        x1, y1, w, h = self.x, self.y, self.width, self.height
        x2, y2 = x1 + w, y1 + w
        w1, h1, w2, h2 = canvasBounds
        if x1<w2 and x2>w1 and y1<h2 and y2>h1:
            if x1<w1: x1 = w1
            if x2>w2: x2 = w2
            if y1<h1: y1 = h1
            if y2>h2: y2 = h2
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)

    def drawPropertyBox(self, canvas):
        if self.displayPropertyBox:
            x1,y1,x2,y2 = self.propertyBoxBounds
            canvas.create_rectangle(x1,y1,x2,y2,fill="white")
            self.drawProperties(canvas)

    def drawProperties(self, canvas):
        x1,y1,x2,y2 = self.propertyBoxBounds
        centerX = (x1+x2)//2
        space = 20
        canvas.create_text(centerX,y1+1*space, text="Name: "+self.name)
        canvas.create_text(centerX,y1+2*space, text="X Position: "+str(self.x))
        canvas.create_text(centerX,y1+3*space, text="Y Position: "+str(self.y))
        canvas.create_text(centerX,y1+4*space, text="Width: "+str(self.width))
        canvas.create_text(centerX,y1+5*space, text="Height: "+str(self.height))