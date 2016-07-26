from class_textbox import *
from class_figure import *
from class_variableInstance import *
import random

####################################
# Block Class
####################################

class Block(object):

    def __init__(self,x,y,w,h,c="None",t="block",text=""):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.dx = 0
        self.dy = 0
        self.drag = False
        self.overlap = False
        self.running = False
        self.type = t
        self.textboxes = []
        self.front = False
        self.inQueue = False
        self.ran = False
        self.posTag = None
        self.endTag = None
        self.rx = 0 
        self.ry = 0
        self.text = text
        self.display = False

    def reset(self,trashcan,blocks,variables=None):
    #'deselects' and 'unconnects' blocks and deletes ones in trashcan
        self.drag, self.overlap = False, False
        if self.isInTrashcan(trashcan) and self.type != "start":
            blocks.remove(self)

    def wasClicked(self,x,y):
    #returns True if the figure was clicked
        return (self.x < x < self.x + self.width and 
                self.y < y < self.y + self.height)

    def blockInBounds(self,canvasBounds): 
    #determines if the block has left the canvas
        x1, y1  = self.x, self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        w1, h1, w2, h2 = canvasBounds
        return x1>w1 and x2<w2 and y1>h1 and y2<h2

    def isInTrashcan(self,trashcan):
    #determines if blic is in trashcan
        w1, w2 = trashcan.x1, trashcan.x2
        h1, h2 = trashcan.y1, trashcan.y2
        x1, y1 = self.x, self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        return (((w1<x1<w2) and (h1<y1<h2)) or ((w1<x2<w2) and (h1<y2<h2)) or
                ((w1<x1<w2) and (h1<y2<h2)) or ((w1<x2<w2) and (h1<y1<h2)) or
                (x1<w1 and x2>w2 and (h1<y1<h2 or h1<y2<h2)) or 
                (y1<h1 and y2>h2 and (w1<x1<w2 or w1<x2<w2)))
    
    def __repr__(self):
        typeName = type(self).__name__
        if typeName == "Block":
            return "%s Block at (%d,%d)" %(self.color,self.x,self.y)
        else:
            return "%s at (%d,%d)" %(typeName,self.x,self.y)       

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
                        if otherBox.text =="": otherBox.text = otherBox.defaultText
        if not oneWasClicked:
            for box in self.textboxes:
                box.allowChange = False
                box.wasClicked = False
                if box.text == "": box.text = box.defaultText
        return oneWasClicked

    def typeParams(self,keysym): 
        for textbox in self.textboxes:
            if textbox.allowChange:
                textbox.type(keysym)

    def copy(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        c = self.color
        t = self.type
        copy = Block(x,y,w,h,c,t)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.display = self.display
        return copy

    #overridden methods
    def run(self,data): 
        block.ran = True
    def moveTextbox(self): pass
    def updateParams(self,data): pass
    def grow(self,x,y): pass
    def shrink(self,x,y): pass
    def setTarget(self): pass

    @staticmethod
    def isInBounds(x1,y1,x2,y2,canvasBounds):
        w1, h1, w2, h2 = canvasBounds
        return x1>=w1 and x2<=w2 and y1>=h1 and y2<=h2

    @staticmethod
    def changeBounds(x1,y1,x2,y2,canvasBounds):
        if y1 < canvasBounds[1] and y2 > canvasBounds[1]: y1 = canvasBounds[1]
        if y2 > canvasBounds[3] and y1 < canvasBounds[3]: y2 = canvasBounds[3]
        if x1 < canvasBounds[0] and x2 > canvasBounds[0]: x1 = canvasBounds[0]
        if x2 > canvasBounds[2] and x1 < canvasBounds[2]: x2 = canvasBounds[2]
        return x1,y1,x2,y2

    #######################
    # Block Motion
    #######################

    def panScreen(self,event,canvasBounds,clickedBlock,newBlock): 
    #moves the block on the canvas to simulate panning
        if not self.drag and not self.overlap and clickedBlock != None and not newBlock:
            #note: does not pan when placing new blocks
            #note: can pan things into the trash
            self.moveTextbox()
            x1, y1 = clickedBlock.x, clickedBlock.y
            x2, y2 = x1 + clickedBlock.width, y1 + clickedBlock.height
            w1, h1, w2, h2 = canvasBounds
            if   x1<w1: self.x += 1
            elif x2>w2: self.x -= 1
            if   y1<h1: self.y += 1
            elif y2>h2: self.y -= 1

    def moveConnected(self,x,y,clickedBlock,line):
    #moves blocks touching the clicked block
        clickedBlock = self.moveFree(x,y,clickedBlock,142)
        #print("line",line,"moveConnected", self)
        #print(self.x,self.y,end="-->")
        if self.overlap:
            self.x = x - self.dx
            self.y = y - self.dy
            self.moveTextbox()
        #print(self.x,self.y)
        return clickedBlock

    def moveFree(self,x,y,clickedBlock,line):
    #moves a clicked block
        #print("line",line,"moveFree", self)
        #print(self.x,self.y,end="-->")
        if self.drag:
            self.x = x - self.dx
            self.y = y - self.dy
            clickedBlock = self
            self.moveTextbox()
        #print(self.x,self.y)
        return clickedBlock

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w, h = self.x, self.y, self.width, self.height
        if (x1<=x<=x1+w) and (y1<=y<=y1+h):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def connect(self,x,y,blocksList):
    #connects all the blocks starting at the clicked block
        x1, y1, w, h = self.x, self.y, self.width, self.height
        if (x1<=x<=x1+w) and (y1<=y<=y1+h):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = True
            self.findConnected(blocksList,x,y)

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if ((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                    (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def snapToGrid(self):
    #snaps blocks to a 10x10px grid
        self.x = (self.x)//10 *10
        self.y = (self.y)//10 *10
        self.moveTextbox()

    #######################
    # Block Drawing
    #######################

    def draw(self,canvas,canvasBounds,trashcan):
        x1,y1,w,h = self.x, self.y, self.width, self.height
        c = self.color
        if self.blockInBounds(canvasBounds):
            if self.isInTrashcan(trashcan) and self.type != "start": c="gray"
            canvas.create_rectangle(x1,y1,x1+w,y1+h,fill=c)
            canvas.create_text(x1+w//2,y1+h//2,text=self.text)
        else:
            self.drawPartialBlock(canvas, canvasBounds, trashcan)
        return c

    def drawPartialBlock(self,canvas,canvasBounds,trashcan):
        x1, y1, w, h = self.x, self.y, self.width, self.height
        x2, y2 = x1 + w, y1 + h
        w1, h1, w2, h2 = canvasBounds
        c = self.color
        if x1<w2 and x2>w1 and y1<h2 and y2>h1:
            if x1<w1: x1 = w1
            if x2>w2: x2 = w2
            if y1<h1: y1 = h1
            if y2>h2: y2 = h2
            if self.isInTrashcan(trashcan) and self.type != "start": c="gray"
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)

####################################
# If Block Class
####################################

class IfBlock(Block):

    def __init__(self,x,y,variables):
        self.variables = variables
        self.w1 = 210
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "indianred1"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"indianred4","grow")
        self.name = None
        self.variableBlock = None
        self.currentLoop = 0
        self.loops = 1
        self.result = None
        self.variableBox = DropBox(self.x+30, self.y+self.margin,70,self.h1//2,variables,"Variables")
        options = ["True","False"]
        self.resultBox = DropBox(self.x+130, self.y+self.margin,70,self.h1//2,options,"Condition")
        self.textboxes = [self.variableBox,self.resultBox]

    def copy(self):
        x = self.x
        y = self.y
        v = self.variables
        copy = IfBlock(x,y,v)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.loops = self.loops
        copy.name = self.name
        copy.variableBlock = self.variableBlock
        copy.result = self.result
        copy.variableBox = self.variableBox
        copy.resultBox = self.resultBox
        copy.textboxes = self.textboxes
        copy.growButton = self.growButton
        copy.currentLoop = self.currentLoop
        return copy

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.variableBox.x = self.x + 30
        self.variableBox.y = self.y + self.margin
        self.resultBox.x = self.x + 130
        self.resultBox.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5 

    def updateParams(self,data):
        self.name = self.variableBox.text
        self.result = self.resultBox.text

    def evaluate(self,variables):
        self.ran = True
        print("   evaluating...",end="")
        for var in variables:
            if var.name == self.name.name:
                self.variableBlock = var
        print(self.variableBlock.value, "?=", self.result, ":", self.variableBlock.value == self.result)
        return self.variableBlock.value == self.result

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+110,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="is", anchor=W)
        #left bar
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        #bottom bar
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# If Block Class
####################################

class IfMathBlock(Block):

    def __init__(self,x,y,variables):
        self.variables = variables
        self.w1 = 220
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "indianred1"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"indianred4","grow")
        self.name = None
        self.variableBlock = None
        self.currentLoop = 0
        self.loops = 1
        self.operator = None
        self.number = 0
        self.variableBox = DropBox(self.x+30, self.y+self.margin,70,self.h1//2,variables,"Variables")
        options = ["=","<",">",">=","<="]
        self.mathBox = DropBox(self.x+110, self.y+self.margin,30,self.h1//2,options,"=")
        self.numberBox = TextBox(self.x+150,self.y+self.margin,60,self.h1//2,"Number")
        self.textboxes = [self.variableBox,self.mathBox,self.numberBox]

    def copy(self):
        x = self.x
        y = self.y
        v = self.variables
        copy = IfMathBlock(x,y,v)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.loops = self.loops
        copy.name = self.name
        copy.variableBlock = self.variableBlock
        copy.operator = self.operator
        copy.number = self.number
        copy.variableBox = self.variableBox
        copy.mathBox = self.mathBox
        copy.numberBox = self.numberBox
        copy.textboxes = self.textboxes
        copy.growButton = self.growButton
        copy.currentLoop = self.currentLoop
        return copy

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.variableBox.x = self.x + 30
        self.variableBox.y = self.y + self.margin
        self.mathBox.x = self.x + 110
        self.mathBox.y = self.y + self.margin
        self.numberBox.x = self.x + 150
        self.numberBox.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5 

    def updateParams(self,data):
        self.name = self.variableBox.text
        try: self.number = int(self.numberBox.text)
        except: pass
        self.operator = self.mathBox.text

    def evaluate(self,variables):
        self.ran = True
        for var in variables:
            if var.name == self.name.name:
                self.variableBlock = var
                try: self.variableBlock.value = int(self.variableBlock.value)
                except: pass
        #print(self.variableBlock.value, self.operator, self.number, end=" : ")
        if self.operator == "=":
            return self.variableBlock.value == self.number
        elif self.operator == "<":
            return self.variableBlock.value < self.number
        elif self.operator == "<=":
            return self.variableBlock.value <= self.number
        elif self.operator == ">":
            return self.variableBlock.value > self.number
        elif self.operator == ">=":
            return self.variableBlock.value >= self.number

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+110,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="is", anchor=W)
        #left bar
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        #bottom bar
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# If Block Class
####################################

class IfTouchingBlock(Block):

    def __init__(self,x,y,figures):
        self.f = figures
        self.w1 = 240
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "indianred1"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"indianred4","grow")
        self.name = None
        self.variableBlock = None
        self.currentLoop = 0
        self.loops = 1
        self.figure1 = None
        self.figure2 = None
        self.selectFigure1Box = DropBox(self.x+30, self.y+self.margin,60,self.height//2,figures,"Figure 1")
        self.selectFigure2Box = DropBox(self.x+170, self.y+self.margin,60,self.height//2,figures,"Figure 2")
        self.textboxes = [self.selectFigure1Box, self.selectFigure2Box]
        self.wasTrue = False

    def copy(self):
        x = self.x
        y = self.y
        f = self.f
        copy = IfTouchingBlock(x,y,f)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.name = self.name
        copy.figure1 = self.figure1
        copy.figure2 = self.figure2
        copy.selectFigure1Box = self.selectFigure1Box
        copy.selectFigure2Box = self.selectFigure2Box
        copy.textboxes = self.textboxes
        copy.growButton = self.growButton
        copy.currentLoop = self.currentLoop
        copy.loops = self.loops
        copy.wasTrue = self.wasTrue
        return copy

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.selectFigure1Box.x = self.x + 30
        self.selectFigure1Box.y = self.y + self.margin
        self.selectFigure2Box.x = self.x + 170
        self.selectFigure2Box.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5 

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigure1Box.text:
                self.figure1 = figure
            elif figure == self.selectFigure2Box.text:
                self.figure2 = figure

    def evaluate(self,variables):
        self.currentLoop += 1
        #print("   evaluating",self.figure1, "touching", self.figure2, ":", end=" ")
        a1,b1,c1,d1 = self.figure1.x, self.figure1.y, self.figure1.x + self.figure1.width, self.figure1.y + self.figure1.height
        a2,b2,c2,d2 = self.figure2.x, self.figure2.y, self.figure2.x + self.figure2.width, self.figure2.y + self.figure2.height
        one = b1<b2<d1
        two = a1<a2<c1
        three = b1<d2<d1
        four = a2<a1<c2
        #print((one and (two or four)) or (three and (two or four)))
        return (one and (two or four)) or (three and (two or four))

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+100,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="is touching", anchor=W)
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# If Block Class
####################################

class IfElseBlock(Block):

    def __init__(self,x,y,variables):
        self.variables = variables
        self.w1 = 230
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "indianred1"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 120
        self.h25 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h25
        self.w3 = 100
        self.h3 = 40
        self.x4 = self.x
        self.y4 = self.y2+self.h2
        self.w4 = 80
        self.h4 = 20
        self.growIfButton = MyButton(self.x+85,self.y+85,10,10,"indianred4","growIf")
        self.growElseButton = MyButton(self.x+65,self.y+165,10,10,"indianred4","growElse")
        self.name = None
        self.variableBlock = None
        self.currentLoop = 0
        self.loops = 1
        self.result = None
        self.variableBox = DropBox(self.x+30, self.y+self.margin,70,self.h1//2,variables,"Variables")
        options = ["True","False"]
        self.resultBox = DropBox(self.x+130, self.y+self.margin,70,self.h1//2,options,"Condition")
        self.textboxes = [self.variableBox,self.resultBox]

    def copy(self):
        x = self.x
        y = self.y
        v = self.variables
        copy = IfElseBlock(x,y,v)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.x4 = self.x4
        copy.y4 = self.y4
        copy.w4 = self.w4
        self.h4 = self.h4
        copy.loops = self.loops
        copy.name = self.name
        copy.variableBlock = self.variableBlock
        copy.result = self.result
        copy.variableBox = self.variableBox
        copy.resultBox = self.resultBox
        copy.textboxes = self.textboxes
        copy.growIfButton = self.growIfButton
        copy.growElseButton = self.growElseButton
        copy.currentLoop = self.currentLoop
        return copy 

    def grow(self,x,y):
        if self.growIfButton.wasClicked(x,y):
            self.h2 += 20
            self.h25 += 20
        if self.growElseButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growIfButton.wasClicked(x,y):
            if self.y3-20 >= self.y+self.h1:
                self.h2 -= 20
                self.h25 -= 20
        if self.growElseButton.wasClicked(x,y):
            if self.y4-20 >= self.y3+self.h3:
                self.h2 -= 20

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def findConnected(self,blocksList,xClick=0,yClick=0): #FIXXX
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        x4, y4, w4, h4 = self.x4, self.y4, self.w4, self.h4
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1)))) or 
                    ((((x1>=x4) and (x1<=x4+w4)) or ((x4>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y4) and (y1<=y4+h4)) or ((y4>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.variableBox.x = self.x + 30
        self.variableBox.y = self.y + self.margin
        self.resultBox.x = self.x + 130
        self.resultBox.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h25
        self.x4 = self.x
        self.y4 = self.y2 + self.h2
        self.growIfButton.x = self.x+85
        self.growIfButton.y = self.y+self.h1+self.h25+5
        self.growElseButton.x = self.x+65
        self.growElseButton.y = self.y+self.h1+self.h2+5 

    def updateParams(self,data):
        self.name = self.variableBox.text
        self.result = self.resultBox.text

    def evaluate(self,variables):
        self.ran = True
        #print("   evaluating...",end="")
        for var in variables:
            if var.name == self.name.name:
                self.variableBlock = var
        #print(self.variableBlock.value, "?=", self.result, ":", self.variableBlock.value == self.result)
        return self.variableBlock.value == self.result

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+110,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="is", anchor=W)
        x1,y1 = self.x+210, self.y+self.h1//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "do", anchor=W)
        #left side
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        #otherwise do
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            self.growIfButton.draw(canvas)
        x1,y1 = self.x+self.margin, self.y3+self.h3//2
        x2,y2 = x1+80,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Otherwise do", anchor=W)
        #end if/else
        x1,y1,x2,y2 = self.x4,self.y4,self.x4+self.w4,self.y4+self.h4
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            self.growElseButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# If KeyPressed Block Class
####################################

class IfKeyPressedBlock(Block):

    def __init__(self,x,y):
        self.w1 = 150
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "indianred1"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"indianred4","grow")
        self.key = None
        self.currentLoop = 0
        self.keyBox = TextBox(self.x+30, self.y+self.margin,30,self.h1//2,"A")
        self.textboxes = [self.keyBox]

    def copy(self):
        x = self.x
        y = self.y
        copy = IfKeyPressedBlock(x,y)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.growButton = self.growButton
        copy.key = self.key
        copy.keyBox = self.keyBox
        copy.textboxes = self.textboxes
        return copy

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.keyBox.x = self.x + 30 
        self.keyBox.y = self.y + 10
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5 

    def updateParams(self,data):
        self.key = self.keyBox.text

    def evaluate(self,key):
        #print("   evaluating",self.key,"==",key,":",self.key==key)
        if self.key != None and key != None: 
            return self.key.upper() == key.upper()
        else:
            return False

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+70,self.y+self.height//2
        x2,y2 = x1+100,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="key is pressed", anchor=W)
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# IfArrowKeyPressed Block Class
####################################

class IfArrowKeyPressedBlock(Block):

    def __init__(self,x,y):
        self.w1 = 170
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "indianred1"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"indianred4","grow")
        self.key = None
        self.currentLoop = 0
        o = ["Up","Down","Left","Right"]
        self.keyBox = DropBox(self.x+30, self.y+self.margin,50,self.h1//2,o,"Up")
        self.textboxes = [self.keyBox]

    def copy(self):
        x = self.x
        y = self.y
        copy = IfArrowKeyPressedBlock(x,y)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.growButton = self.growButton
        copy.key = self.key
        copy.keyBox = self.keyBox
        copy.textboxes = self.textboxes
        return copy

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.keyBox.x = self.x + 30 
        self.keyBox.y = self.y + 10
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5 

    def updateParams(self,data):
        self.key = self.keyBox.text

    def evaluate(self,key):
        #print("   evaluating",self.key,"==",key,":",self.key==key)
        return self.key == key

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+90,self.y+self.height//2
        x2,y2 = x1+100,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="key is pressed", anchor=W)
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# Variable Block Class
####################################

class VariableBlock(Block):

    def __init__(self,x,y,n="Variable",v="True"):
        self.width = 170
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "gold"
        self.name = n
        self.value = v
        self.nameBox = TextBox(self.x+10,self.y+10,60,20,self.name)
        self.valueBox = TextBox(self.x+100,self.y+10,60,20,self.value)
        self.textboxes = [self.nameBox, self.valueBox]
        self.display = False

    def __eq__(self,other):
        if type(other) == VariableBlock:
            return self.name == other.name # and self.value == other.value
        else: return False

    def __repr__(self):
        return str(self.name) 

    def reset(self,trashcan,blocks,variables):
    #'deselects' and 'unconnects' blocks and deletes ones in trashcan
        self.drag, self.overlap = False, False
        if self.isInTrashcan(trashcan) and self.type != "start":
            blocks.remove(self)
            variables.remove(self)

    def copy(self):
        x = self.x
        y = self.y
        n = self.nameBox
        v = self.value
        copy = VariableBlock(x,y,n,v)
        copy.width = self.width
        copy.height = self.height
        copy.margin = self.margin
        copy.color = self.color
        copy.nameBox = self.nameBox
        copy.valueBox = self.valueBox
        copy.textboxes = self.textboxes
        copy.display = self.display
        return copy

    def moveTextbox(self):
        self.nameBox.x = self.x+10
        self.nameBox.y = self.y+self.height//4
        self.valueBox.x = self.x+100
        self.valueBox.y = self.y+self.height//4

    def updateParams(self,data):
        self.name = self.nameBox.text
        self.value = self.valueBox.text
        
    def run(self,data):
        self.updateParams(data)
        if self not in data.runVariables:
            data.runVariables.append(self)
        else:
            i = data.runVariables.index(self)
            data.runVariables[i] = self
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+82,self.y+self.height//2
        x2,y2 = x1+5,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "=", anchor=W)

####################################
# Variable Instance Block Class
####################################

class VariableInstanceBlock(Block):

    def __init__(self,x,y,variables,n="Select",v="True"):
        self.width = 195
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "gold"
        self.name = n
        self.value = v
        self.nameBox = DropBox(self.x+35,self.y+10,60,20,variables,self.name)
        self.valueBox = TextBox(self.x+125,self.y+10,60,20,self.value)
        self.textboxes = [self.nameBox, self.valueBox]
        #self.instanceButton = MyButton(self.x+self.width,self.y,10,self.height,"chocolate2","variableInstance")

    def __eq__(self,other):
        if type(other) == VariableInstanceBlock:
            return self.name == other.name # and self.value == other.value
        else: return False

    def __repr__(self):
        tech = super().__repr__()
        return str(self.name) + " " + str(tech)

    def copy(self):
        x = self.x
        y = self.y
        n = self.nameBox
        v = self.value
        copy = VariableInstanceBlock(x,y,n,v)
        copy.width = self.width
        copy.height = self.height
        copy.margin = self.margin
        copy.color = self.color
        copy.nameBox = self.nameBox
        copy.valueBox = self.valueBox
        copy.textboxes = self.textboxes
        return copy

    def moveTextbox(self):
        self.nameBox.x = self.x+35
        self.nameBox.y = self.y+self.height//4
        self.valueBox.x = self.x+125
        self.valueBox.y = self.y+self.height//4

    def updateParams(self,data):
        self.name = self.nameBox.text
        self.value = self.valueBox.text
        
    def run(self,data):
        self.updateParams(data)
        print("   setting",self.name, "to",self.value)
        print("  ",type(self.name))
        for variable in data.runVariables:
            print("    ",variable,self.name==variable)
            if self.name == variable:
                variable.value = self.value
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+10,self.y+self.height//2
        x2,y2 = x1+20,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "Set", anchor=W)
        x1,y1 = self.x+105,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "to", anchor=W)

####################################
# Display Variable Block Class
####################################

class DisplayVariableBlock(Block):

    def __init__(self,x,y,variables,n="Variable"):
        self.width = 130
        self.height = 40
        self.margin = 10
        self.v = variables
        super().__init__(x,y,self.width,self.height)
        self.color = "gold"
        self.name = n
        self.nameBox = DropBox(self.x+60,self.y+10,60,20,variables,self.name)
        self.textboxes = [self.nameBox]
        self.display = False

    def __eq__(self,other):
        if type(other) == DisplayVariableBlock:
            return self.name == other.name # and self.value == other.value
        else: return False

    def copy(self):
        x = self.x
        y = self.y
        n = self.name
        v = self.v
        copy = DisplayVariableBlock(x,y,v,n)
        copy.width = self.width
        copy.height = self.height
        copy.margin = self.margin
        copy.color = self.color
        copy.nameBox = self.nameBox
        copy.textboxes = self.textboxes
        copy.variable = self.variable
        copy.display = self.display
        return copy

    def moveTextbox(self):
        self.nameBox.x = self.x+60
        self.nameBox.y = self.y+self.height//4

    def updateParams(self,data):
        self.name = self.nameBox.text
        self.variable = None
        for var in data.runVariables:
            if type(self.name) == VariableBlock and var.name == self.name.name:
                self.variable = var

    def reset(self,trashcan,blocks,variables=None):
        super().reset(trashcan,blocks,variables)
        try: self.variable.display = False
        except: pass

    def run(self,data):
        self.updateParams(data)
        self.variable.display = True
        count = DisplayVariableBlock.getYPos(data, self.variable)
        x = data.screenBounds[0] + 20
        y = data.screenBounds[1] + 30*count - 10
        w = max((len(str(self.name)) + len(str(self.variable.value)))*10,50)
        figure = Figure(x,y,w,20,"gold",self.name,data.propertyBoxBounds,data,self.variable)
        if figure in data.figureCopies:
            data.figureCopies.remove(figure)
        data.figureCopies.append(figure)
        #print("FIGURES:",data.figureCopies)
        self.ran = True

    @staticmethod
    def getYPos(data, variable):
        count = 0
        for var in data.runVariables:
            count += 1
            if variable == var: return count
        return count

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+10,self.y+self.height//2
        x2,y2 = x1+20,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "Display", anchor=W)

####################################
# Change Variable Block Class
####################################

class ChangeVariableBlock(Block):

    def __init__(self,x,y,variables,n="Variable",v=0):
        self.width = 185
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "gold"
        self.name = n
        self.variable = None
        self.value = v
        self.nameBox = DropBox(self.x+60,self.y+10,60,20,variables,self.name)
        self.valueBox = TextBox(self.x+150,self.y+10,25,20,self.value)
        self.textboxes = [self.nameBox, self.valueBox]

    def __eq__(self,other):
        if type(other) == ChangeVariableBlock:
            return self.x == other.x and self.y == other.y # and self.value == other.value
        else: return False

    def __repr__(self):
        return str(self.name)

    def copy(self):
        x = self.x
        y = self.y
        n = self.nameBox
        v = self.value
        copy = ChangeVariableBlock(x,y,n,v)
        copy.width = self.width
        copy.height = self.height
        copy.margin = self.margin
        copy.color = self.color
        copy.nameBox = self.nameBox
        copy.valueBox = self.valueBox
        copy.textboxes = self.textboxes
        return copy

    def moveTextbox(self):
        self.nameBox.x = self.x+60
        self.nameBox.y = self.y+self.height//4
        self.valueBox.x = self.x+150
        self.valueBox.y = self.y+self.height//4

    def updateParams(self,data):
        self.name = self.nameBox.text
        try: self.value = int(self.valueBox.text)
        except: pass
        
    def run(self,data):
        self.updateParams(data)
        for var in data.runVariables:
            if self.name == var:
                try:
                    val = int(var.value) 
                    val += int(self.value)
                    var.value = val
                    #print("  ",var, var.value)
                except: pass
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+10,self.y+self.height//2
        x2,y2 = x1+20,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "Change", anchor=W)
        x1,y1 = self.x+130,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "by", anchor=W)

####################################
# Loop Block Class
####################################

class LoopBlock(Block):

    def __init__(self,x,y):
        self.w1 = 160
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "mediumorchid2"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.loops = 0
        self.currentLoop = 0
        self.selectLoopsBox = TextBox(self.x+50, self.y+self.margin,60,self.h1//2,"Number")
        self.textboxes = [self.selectLoopsBox]
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"mediumorchid4","grow")

    def copy(self):
        x = self.x
        y = self.y
        copy = LoopBlock(x,y)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.loops = self.loops
        copy.currentLoop = self.currentLoop
        copy.selectLoopsBox = self.selectLoopsBox
        copy.textboxes = self.textboxes
        copy.growButton = self.growButton
        copy.posTag = self.posTag
        copy.endTag = self.endTag
        return copy

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def run(self,data):
        self.currentLoop = 0
        self.ran = True

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.selectLoopsBox.x = self.x + 50
        self.selectLoopsBox.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5

    def updateParams(self,data):
    #updates the objects properties based on the blocks parameters
        try: self.loops = int(self.selectLoopsBox.text)-1
        except: pass

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Loop", anchor=W)
        x1,y1 = self.x+120,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="times", anchor=W)
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# While Loop Block Class
####################################

class WhileLoopBlock(Block):

    def __init__(self,x,y,variables):
        self.w1 = 230
        self.h1 = 40
        self.margin = 10
        self.v = variables
        super().__init__(x,y,self.w1,self.h1)
        self.color = "mediumorchid2"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.name = None
        self.result = None
        self.currentLoop = 0
        self.selectVariableBox = DropBox(self.x+50, self.y+self.margin,70,self.h1//2,variables,"Select")
        self.selectResultBox = TextBox(self.x+150,self.y+self.margin,70,self.h1//2,"Condition")
        self.textboxes = [self.selectVariableBox, self.selectResultBox]
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"mediumorchid4","grow")

    def copy(self):
        x = self.x
        y = self.y
        v = self.v
        copy = WhileLoopBlock(x,y,v)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.selectVariableBox = self.selectVariableBox
        copy.selectResultBox = self.selectResultBox
        copy.textboxes = self.textboxes
        copy.growButton = self.growButton
        copy.posTag = self.posTag
        copy.endTag = self.endTag
        return copy

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def run(self,data):
        self.currentLoop = 0
        self.ran = True

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.selectVariableBox.x = self.x + 50
        self.selectVariableBox.y = self.y + self.margin
        self.selectResultBox.x = self.x + 150
        self.selectResultBox.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5

    def updateParams(self,data):
    #updates the objects properties based on the blocks parameters
        self.name = self.selectVariableBox.text 
        self.result = self.selectResultBox.text

    def evaluate(self,variables):
        self.ran = True
        for var in variables:
            if var.name == self.name.name:
                self.variableBlock = var
        return self.variableBlock.value == self.result

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "While", anchor=W)
        x1,y1 = self.x+130,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="is", anchor=W)
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)

####################################
# Forever Loop Block Class
####################################

class ForeverLoopBlock(Block):

    def __init__(self,x,y):
        self.w1 = 90
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "mediumorchid2"
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.w2 = 20
        self.h2 = 40
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.w3 = 80
        self.h3 = 20
        self.currentLoop = 0
        self.growButton = MyButton(self.x+65,self.y+85,10,10,"mediumorchid4","grow")

    def copy(self):
        x = self.x
        y = self.y
        copy = ForeverLoopBlock(x,y)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.growButton = self.growButton
        return copy

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
        x3, y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        if (((x1<=x<=x1+w1) and (y1<=y<=y1+h1)) or 
            ((x2<=x<=x2+w2) and (y2<=y<=y2+h2)) or
            ((x3<=x<=x3+w3) and (y3<=y<=y3+h3))):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False
            self.front = True

    def grow(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 += 20

    def shrink(self,x,y):
        if self.growButton.wasClicked(x,y):
            self.h2 -= 20

    def run(self,data):
        self.currentLoop = 0
        self.ran = True

    def findConnected(self,blocksList,xClick=0,yClick=0): 
    #uses recursion to figure out which blocks are connected
        x, y, w, h = self.x, self.y, self.width, self.height
        x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
        for block in blocksList:
            if not block.overlap:
                x1, y1 = block.x, block.y
                w1, h1 = block.width, block.height
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or 
                    ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                     (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))):
                    block.overlap = True
                    block.dx = xClick - x1
                    block.dy = yClick - y1
                    block.findConnected(blocksList, xClick, yClick)

    def moveTextbox(self):
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+80,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Loop forever", anchor=W)
        x1,y1,x2,y2 = self.x2,self.y2,self.x2+self.w2,self.y2+self.h2
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
        x1,y1,x2,y2 = self.x3,self.y3,self.x3+self.w3,self.y3+self.h3
        x1,y1,x2,y2 = Block.changeBounds(x1,y1,x2,y2,canvasBounds)
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)
            if x2 < canvasBounds[2]-15 and y1 > canvasBounds[1]-15 and x2 > canvasBounds[0] + 15:
                self.growButton.draw(canvas)

####################################
# Edge Bounce Block Class
####################################

class EdgeBounceBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 210
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure = None
        self.selectFigureBox = DropBox(self.x+10, self.y+self.margin,100,self.height//2,figures,"Figure")
        self.textboxes = [self.selectFigureBox]
        self.direction = None

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = EdgeBounceBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.figure = self.figure
        copy.selectFigureBox = self.selectFigureBox
        return copy

    def moveTextbox(self):
        self.selectFigureBox.x = self.x + 10
        self.selectFigureBox.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure

    def run(self,data):
        self.figure.checkEdge = True
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+120,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "bounce off wall", anchor=W)

####################################
# Edge Bounce Block Class
####################################

class BounceBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 130
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure = None
        self.selectFigureBox = DropBox(self.x+10, self.y+self.margin,60,self.height//2,figures,"Figure")
        self.textboxes = [self.selectFigureBox]
        self.direction = None

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = BounceBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.figure = self.figure
        copy.selectFigureBox = self.selectFigureBox
        return copy

    def moveTextbox(self):
        self.selectFigureBox.x = self.x + 10
        self.selectFigureBox.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure

    def run(self,data):
        #print("   ",self.rx, self.ry,end=" --> ")
        self.rx = -self.rx
        self.ry = -self.ry
        #print(self.rx, self.ry)
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+80,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "bounce", anchor=W)

####################################
# Bounce Random Block Class
####################################

class BounceRandomBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 190
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure = None
        self.selectFigureBox = DropBox(self.x+60, self.y+self.margin,60,self.height//2,figures,"Figure")
        self.textboxes = [self.selectFigureBox]
        self.direction = None

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = BounceRandomBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.figure = self.figure
        copy.selectFigureBox = self.selectFigureBox
        return copy

    def moveTextbox(self):
        self.selectFigureBox.x = self.x + 60
        self.selectFigureBox.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure

    def run(self,data):
        if self.rx == 0 and self.ry == 0:
            self.rx = random.randint(5,10)*random.choice([-1,1])
            self.ry = random.randint(5,10)*random.choice([-1,1])
        if self.figure.x < data.screenBounds[0] or self.figure.x+self.figure.width > data.screenBounds[2] :
            self.rx = -self.rx
        if self.figure.y < data.screenBounds[1] or self.figure.y+self.figure.height > data.screenBounds[3] :
            self.ry = -self.ry
        self.figure.x += self.rx
        self.figure.y += self.ry
        #print("  ",self.rx,self.ry)
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+10,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "Move", anchor=W)
        x1,y1 = self.x+130,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "randomly", anchor=W)

####################################
# Move Towards Block Class
####################################

class MoveTowardsBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 320
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure1 = None
        self.figure2 = None
        self.selectFigure1Box = DropBox(self.x+50, self.y+self.margin,100,self.height//2,figures,"Figure 1")
        self.selectFigure2Box = DropBox(self.x+210, self.y+self.margin,100,self.height//2,figures,"Figure 2")
        self.textboxes = [self.selectFigure1Box, self.selectFigure2Box]

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = MoveTowardsBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.figure1 = self.figure1
        copy.figure2 = self.figure2
        copy.selectFigure1Box = self.selectFigure1Box
        copy.selectFigure2Box = self.selectFigure2Box
        return copy

    def moveTextbox(self):
        self.selectFigure1Box.x = self.x + 50
        self.selectFigure1Box.y = self.y + self.margin
        self.selectFigure2Box.x = self.x + 210
        self.selectFigure2Box.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigure1Box.text:
                self.figure1 = figure
            elif figure == self.selectFigure2Box.text:
                self.figure2 = figure

    def run(self,data):
        totalX = self.figure2.x - self.figure1.x
        totalY = self.figure2.y - self.figure1.y
        dx = totalX//10
        dy = totalY//10
        self.figure1.x += dx
        self.figure1.y += dy
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+10, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Move", anchor=W)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+160,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "towards", anchor=W)

####################################
# Move Block Class
####################################

class MoveBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 350
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.direction = ""
        self.pixels = 0
        self.figure = None
        self.selectFigureBox = DropBox(self.x+50, self.y+self.margin,100,self.height//2,figures,"Figure")
        dirOptions = ["Up","Down","Left","Right"]
        self.selectDirectionBox = DropBox(self.x+160, self.y+self.margin,70,self.height//2, dirOptions,"Direction")
        self.selectPixelsBox = TextBox(self.x+240, self.y+self.margin,60,self.height//2,"Number")
        self.textboxes = [self.selectFigureBox,self.selectDirectionBox,self.selectPixelsBox]
        self.checkEdge = False
        self.target = 0

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = MoveBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.direction = self.direction
        copy.pixels = self.pixels
        copy.figure = self.figure
        copy.target = self.target
        copy.selectFigureBox = self.selectFigureBox
        copy.selectPixelsBox = self.selectPixelsBox
        copy.selectDirectionBox = self.selectDirectionBox
        copy.checkEdge = self.checkEdge
        copy.target = self.target
        return copy

    def moveTextbox(self):
    #adjusts the textboxes to move with the block 
        self.selectFigureBox.x = self.x + 50
        self.selectFigureBox.y = self.y + self.margin
        self.selectDirectionBox.x = self.x + 160
        self.selectDirectionBox.y = self.y + self.margin
        self.selectPixelsBox.x = self.x + 240
        self.selectPixelsBox.y = self.y + self.margin

    def updateParams(self,data):
    #updates the objects properties based on the blocks parameters
        self.direction = self.selectDirectionBox.text
        try: self.pixels = int(self.selectPixelsBox.text)
        except: pass
        self.figure = self.selectFigureBox.text
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure
                self.figure.direction = self.direction
        self.setTarget()

    def setTarget(self):
        if not self.ran and type(self.figure)==Figure:
            if self.direction == "Up":
                self.target = self.figure.y - self.pixels
            elif self.direction == "Down":
                self.target = self.figure.y + self.pixels
            elif self.direction == "Left":
                self.target = self.figure.x - self.pixels
            elif self.direction == "Right":
                self.target = self.figure.x + self.pixels

    def run(self, data):
        if self.direction == "Up":
            if self.figure.y > self.target: 
                delta = abs(self.target-self.figure.y) if abs(self.target-self.figure.y) < 10 else 10
                if self.figure.checkEdge and self.figure.y-delta<data.screenBounds[1]:
                    self.direction = self.figure.direction = "Down"
                    self.target = data.screenBounds[1] + (data.screenBounds[1]-self.target)
                self.figure.runMove(self.direction, delta)
                self.ry = -delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()
        elif self.direction == "Down":
            if self.figure.y < self.target: 
                delta = abs(self.target-self.figure.y) if abs(self.target-self.figure.y) < 10 else 10
                if self.figure.checkEdge and self.figure.y+self.figure.height+delta<data.screenBounds[3]:
                    self.direction = self.figure.direction = "Up"
                    self.target = data.screenBounds[3] - (self.target-data.screenBounds[3])
                self.figure.runMove(self.direction, delta)
                self.ry = delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()
        elif self.direction == "Right":
            if self.figure.x < self.target: 
                delta = abs(self.target-self.figure.x) if abs(self.target-self.figure.x) < 10 else 10
                if self.figure.checkEdge and self.figure.x+self.figure.width+delta>data.screenBounds[2]:
                    self.direction = self.figure.direction = "Left"
                    self.target = data.screenBounds[2] - (self.target-data.screenBounds[2])
                self.figure.runMove(self.direction, delta)
                self.rx = delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()
        elif self.direction == "Left":
            if self.figure.x > self.target: 
                delta = abs(self.target-self.figure.x) if abs(self.target-self.figure.x) < 10 else 10
                if self.figure.checkEdge and self.figure.x-delta<data.screenBounds[0]:
                    self.direction = self.figure.direction = "Right"
                    self.target = data.screenBounds[0] + (data.screenBounds[0]-self.target)
                self.figure.runMove(self.direction, delta)
                self.rx = -delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()

    def draw(self,canvas,canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+10, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Move", anchor=W)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                #canvas.tag_raise(textbox)
                textbox.draw(canvas)
        x1,y1 = self.x+310,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "pixels", anchor=W)

####################################
# Jump Block Class
####################################

class JumpBlock(Block):

    def __init__(self,jumpTo):
        self.jumpTo = jumpTo
        self.endTag = None

    def __repr__(self):
        return "JumpBlock to " + str(self.jumpTo)

    def copy(self):
        j = self.jumpTo
        copy = JumpBlock(j)
        copy.posTag = self.posTag
        return copy

    def run(self,data,endIndex):
        #data.key = None
        for i in range(self.jumpTo,endIndex):
            #print("     resetting:", data.queue[i])
            data.queue[i].ran = False
            data.queue[i].setTarget()
            if i>self.jumpTo and type(data.queue[i]) in {LoopBlock, IfBlock, IfTouchingBlock}:
                data.queue[i].currentLoop = 0
        return self.jumpTo

##################################################################################
##################################################################################
##################################################################################
##################################################################################

####################################
# Button Class
####################################

class MyButton(object):

    def __init__(self,x,y,w,h,c,t,title=""):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.type = t
        self.title=title

    def __repr__(self):
        return "button type: " + str(self.type)

    def wasClicked(self,x,y):
        return ((self.x <= x <= self.x + self.width) and
                (self.y <= y <= self.y + self.height))

    def draw(self,canvas,codeWidth=0,vertical=True):
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        if vertical == None:
            canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
            canvas.create_text(x1+self.width//2,y1+self.height//2,text=self.title)
        elif vertical: 
            canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
            if self.type in {"UI","scroll"}:
                canvas.create_text(x1+self.width//2,y1+self.height//2,text=self.title)
        elif x1<codeWidth:
            if x2 > codeWidth: x2 = codeWidth
            canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
            if x2 < codeWidth:
                canvas.create_text(x1+self.width//2,y1+self.height//2,text=self.title)

####################################
# Figure Button Class
####################################

class FigureButton(MyButton):

    def __init__(self,w,h,c,t,title=""):
        self.x = 0
        self.y = 0
        self.width = w
        self.height = h
        self.color = c
        self.type = t
        self.title = ""

    def createfigure(self,figures,propertyBoxBounds,data):
        x1,y1 = self.x, self.y
        w,h = self.width, self.height
        figure = Figure(x1,y1,w,h,self.color,self.type,propertyBoxBounds,data)
        figure.name += str(len(figures))
        figure.updateParams(data)
        figure.nameBox.defaultText = figure.name
        figures.append(figure)

####################################
# Block Button Class
####################################

class BlockButton(MyButton):

    def __init__(self,x,y,w,h,c,t,title=""):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.type = t
        self.title = title

    def createBlock(self,data,click):
        x1,y1 = self.x, self.y
        w,h = self.width, self.height
        if click < data.codeWidth:
            if self.type == "move": block = MoveBlock(x1,y1,data.figures)
            elif self.type == "loop": block = LoopBlock(x1,y1)
            elif self.type == "movetowards": block = MoveTowardsBlock(x1,y1,data.figures)
            elif self.type == "edgeBounce": block = EdgeBounceBlock(x1,y1,data.figures)
            elif self.type == "instance": block = VariableInstanceBlock(x1,y1,data.variables)
            elif self.type == "if": block = IfBlock(x1,y1,data.variables)
            elif self.type == "while": block = WhileLoopBlock(x1,y1,data.variables)
            elif self.type == "forever": block = ForeverLoopBlock(x1,y1)
            elif self.type == "keypressed": block = IfKeyPressedBlock(x1,y1)
            elif self.type == "ifElse": block = IfElseBlock(x1,y1,data.variables)
            elif self.type == "displayVar": block = DisplayVariableBlock(x1,y1,data.variables)
            elif self.type == "changeVar": block = ChangeVariableBlock(x1,y1,data.variables)
            elif self.type == "bounceRandom": block = BounceRandomBlock(x1,y1,data.figures)
            elif self.type == "ifTouching": block = IfTouchingBlock(x1,y1,data.figures)
            elif self.type == "bounce": block = BounceBlock(x1,y1,data.figures)
            elif self.type == "arrowPressed": block = IfArrowKeyPressedBlock(x1,y1)
            elif self.type == "ifmath": block = IfMathBlock(x1,y1,data.variables)
            elif self.type == "variable": 
                block = VariableBlock(x1,y1)
                data.variables.append(block)
            else: block = Block(x1,y1,w,h,self.color,self.type)
            data.blocks.append(block)