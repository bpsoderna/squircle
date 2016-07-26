from class_figure import *
from class_block import *


####################################
# Figure Class
####################################

class Figure(object):

    def __init__(self,x,y,w,h,c,t,propertyBoxBounds,data,variable=None):
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
        self.nameBox = TextBox(propertyBoxBounds[0]+50,propertyBoxBounds[1]+17,90,20,self.name)
        self.xBox = TextBox(propertyBoxBounds[0]+70,propertyBoxBounds[1]+43,70,20,str(self.x))
        self.yBox = TextBox(propertyBoxBounds[0]+70,propertyBoxBounds[1]+68,70,20,str(self.y))
        self.widthBox = TextBox(propertyBoxBounds[0]+50,propertyBoxBounds[1]+93,90,20,str(self.width))
        self.heightBox = TextBox(propertyBoxBounds[0]+52,propertyBoxBounds[1]+118,88,20,str(self.height))
        self.updateParams(data)
        self.textboxes = [self.nameBox, self.xBox, self.yBox,self.widthBox,self.heightBox]
        self.direction = None
        self.checkEdge = False
        self.var = variable

    #####################
    # Figure Methods
    #####################

    def __repr__(self):
        return str(self.name)

    def __eq__(self,other):
        if type(other) == str:
            return other == self.name
        elif isinstance(other,Figure):
            return self.name == other.name
        else:
            return False

    def copy(self,data, line):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        c = self.color
        t = self.type
        pbb = self.propertyBoxBounds
        copy = Figure(x,y,w,h,c,t,pbb,data)
        copy.drag = self.drag
        copy.dx, copy.dy = self.dx, self.dy
        copy.displayPropertyBox = self.displayPropertyBox
        copy.textboxes = self.textboxes
        copy.name = self.name
        copy.var = self.var
        copy.checkEdge = self.checkEdge
        copy.direction = self.direction
        return copy

    def clicked(self,x,y):
    #returns True if the figure was clicked
        return (self.x < x < self.x + self.width and 
                self.y < y < self.y + self.height)

    def reset(self,trashcan,figures,figureCopies):
    #'unselects' figure and deletes it if it's in the trashcan
        self.drag = False
        self.checkEdge = False
        if self.isInTrashcan(trashcan):
            figures.pop(figures.index(self))
            figureCopies.pop(figureCopies.index(self))

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

    def setParams(self,x,y):
    #sets up textboxes so only one is changed at a time
        oneWasClicked = False
        for box in self.textboxes:
            if box.clicked(x,y):
                oneWasClicked = True
                for otherBox in self.textboxes:
                    if box == otherBox:
                        box.allowChange = True
                        if box.typeError: box.typeError = False
                        elif box.text == box.defaultText:
                            box.text = ""
                    else:
                        otherBox.allowChange = False
                        otherBox.wasClicked = False
                        otherBox.displayPropertyBox = False
                        if otherBox.text == "": otherBox.text = otherBox.defaultText
        if not oneWasClicked:
            for box in self.textboxes:
                box.allowChange = False
                box.wasClicked = False
                if box.text == "": box.text = box.defaultText
        return oneWasClicked

    def updateUserParams(self,data):
        if self.displayPropertyBox:
            self.name = self.nameBox.text
            try: self.x = int(self.xBox.text) + data.canvasBounds[0]
            except: pass
            try: self.y = int(self.yBox.text) + data.canvasBounds[1]
            except: pass
            try: self.width = int(self.widthBox.text)
            except: pass
            try: self.height = int(self.heightBox.text)
            except: pass
        Figure.copyFigures(data)

    def updateParams(self,data):
        self.xBox.text = str(self.x - data.canvasBounds[0])
        self.nameBox.text = self.name
        self.yBox.text = str(self.y - data.canvasBounds[1])

    def typeParams(self,keysym):
    #if a textbox was clicked, type in it
        if self.displayPropertyBox:
            for box in self.textboxes:
                if box.allowChange:
                    box.type(keysym)

    @staticmethod
    def copyFigures(data):
        dx = data.canvasBounds[0] - data.screenBounds[0]
        dy = data.canvasBounds[1] - data.screenBounds[1] 
        data.figureCopies = []
        for figure in data.figures:
            tempFig = figure.copy(data, 157)
            tempFig.x -= dx
            tempFig.y -= dy
            data.figureCopies.append(tempFig)

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
        else: pass

    #####################
    # Figure Motion
    #####################

    def move(self,x,y,clickedfigure,copy,dx,dy):
    #moves a clicked block
        if self.drag:
            self.x = x - self.dx
            self.y = y - self.dy
            clickedfigure = self
            copy.x = self.x - dx
            copy.y = self.y - dy
        return clickedfigure

    def selectIndividual(self,x,y,figures):
    #selects one clicked block and displays its property box
        x1, y1 = self.x, self.y
        if self.clicked(x,y):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.displayPropertyBox = True
            figures.remove(self)
            figures.append(self)
        elif Figure.clickedPropertyBox(x,y,self.propertyBoxBounds): 
            self.displayPropertyBox = True
        else:
            self.displayPropertyBox = False

    @staticmethod
    def clickedPropertyBox(x,y,propertyBoxBounds):
        x1,y1,x2,y2 = propertyBoxBounds
        return x1<=x<=x2 and y1<=y<=y2

    def panScreen(self,event,canvasBounds,clickedFigure,newFigure,copy,dx,dy): 
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
            copy.x = self.x - dx
            copy.y = self.y - dy

    #####################
    # Figure Drawing
    #####################

    def draw(self,canvas,canvasBounds,trashcan):
        x1,y1,w,h = self.x, self.y, self.width, self.height
        c = self.color
        self.drawPropertyBox(canvas)
        if trashcan != None and self.isInTrashcan(trashcan):
            c = "gray"
        if self.isInBounds(canvasBounds):
            canvas.create_rectangle(x1,y1,x1+w,y1+h,fill=c)
            try:canvas.create_text(x1+w//2,y1+h//2,text=self.var.name+": "+str(self.var.value))
            except: pass
        else:
            self.drawPartialFigure(canvas,canvasBounds,c)

    def drawCopy(self,canvas):
        x1,y1,w,h = self.x, self.y, self.width, self.height
        c = self.color
        if self.type == "rectangle":
            canvas.create_rectangle(x1,y1,x1+w,y1+h,fill=c)

    def drawPartialFigure(self,canvas,canvasBounds,c):
        x1, y1, w, h = self.x, self.y, self.width, self.height
        x2, y2 = x1 + w, y1 + h
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
            canvas.create_rectangle(x1,y1,x2,y2,fill="powderblue")
            self.drawProperties(canvas)

    def drawProperties(self, canvas):
        x1,y1,x2,y2 = self.propertyBoxBounds
        centerX = (x1+x2)//2
        space = 25
        canvas.create_text(x1+10,y1+1*space, text="Name:",anchor=NW)
        canvas.create_text(x1+10,y1+2*space, text="X Position:",anchor=NW)
        canvas.create_text(x1+10,y1+3*space, text="Y Position:",anchor=NW)
        canvas.create_text(x1+10,y1+4*space, text="Width:",anchor=NW)
        canvas.create_text(x1+10,y1+5*space, text="Height:",anchor=NW)
        for box in self.textboxes:
            box.draw(canvas)