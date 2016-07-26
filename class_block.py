from class_textbox import *
from class_button import *

####################################
# Block Class
####################################

class Block(object):

    def __init__(self,x,y,w,h,c="None",t="block"):
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
        self.textBoxes = []

    #######################
    # Block Methods
    #######################

    def reset(self,trashcan,blocks):
    #'deselects' and 'unconnects' blocks and deletes ones in trashcan
        self.drag, self.overlap = False, False
        if self.isInTrashcan(trashcan) and self.type != "start":
            blocks.pop(blocks.index(self))

    def isInBounds(self,canvasBounds): 
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
        return "%s Block at (%d,%d)-%s" %(type(self),self.x,self.y,self.color)

    def setParams(self,x,y):
    #sets up textboxes so only one is changed at a time
        oneWasClicked = False
        for box in self.textBoxes:
            if box.clicked(x,y):
                oneWasClicked = True
                for otherBox in self.textBoxes:
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
            for box in self.textBoxes:
                box.allowChange = False
                if box.text == "": box.text = box.defaultText

    #overridden methods
    def run(self): pass
    def moveTextbox(self): pass
    def typeParams(self,keysym): pass
    def updateParams(self,figures): pass

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

    def moveConnected(self,x,y,clickedBlock):
    #moves blocks touching the clicked block
        clickedBlock = self.moveFree(x,y,clickedBlock)
        if self.overlap:
            self.x = x - self.dx
            self.y = y - self.dy
            self.moveTextbox()
        return clickedBlock

    def moveFree(self,x,y,clickedBlock):
    #moves a clicked block
        if self.drag:
            self.x = x - self.dx
            self.y = y - self.dy
            clickedBlock = self
            #self.moveTextbox()
        return clickedBlock

    def selectIndividual(self,x,y):
    #sets up a clicked block to be moved
        x1, y1, w, h = self.x, self.y, self.width, self.height
        if (x1<=x<=x1+w) and (y1<=y<=y1+h):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = False

    def connect(self,x,y,blocksList):
    #connects all the blocks starting at the clicked block
        x1, y1, w, h = self.x, self.y, self.width, self.height
        if (x1<=x<=x1+w) and (y1<=y<=y1+h):
            self.dx = x - x1
            self.dy = y - y1
            self.drag = True
            self.overlap = True
            self.findConnected(blocksList,x,y)

    def findConnected(self,blocksList,xClick,yClick): 
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
        if self.isInBounds(canvasBounds):
            if self.isInTrashcan(trashcan) and self.type != "start": c="gray"
            elif self.running: c="deeppink"
            canvas.create_rectangle(x1,y1,x1+w,y1+h,fill=c)
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
            elif self.running: c="deeppink"
            canvas.create_rectangle(x1,y1,x2,y2,fill=c)

####################################
# Loop Block Class
####################################

class LoopBlock(Block):

    def __init__(self,x,y):
        self.w1 = 160
        self.h1 = 40
        self.margin = 10
        super().__init__(x,y,self.w1,self.h1)
        self.color = "turquoise1"
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
        self.textBoxes = [self.selectLoopsBox]
        self.growButton = Button(self.x+65,self.y+85,10,10,"white","grow")
        print(self.growButton)

    def run(self):
        pass

    def moveTextbox(self):
        self.selectLoopsBox.x = self.x + 50
        self.selectLoopsBox.y = self.y + self.margin
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+85

    def typeParams(self,keysym):
    #if a textbox was clicked, type in it
        if self.selectLoopsBox.allowChange:
            self.selectLoopsBox.type(keysym)

    def updateParams(self,figures):
    #updates the objects properties based on the blocks parameters
        try: self.loops = int(self.selectLoopsBox.text)
        except: pass

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        canvas.create_text(self.x+self.margin, self.y+self.height//2, text = "Loop", anchor=W)
        self.selectLoopsBox.draw(canvas)
        canvas.create_text(self.x+120,self.y+self.height//2,text="times", anchor=W)
        canvas.create_rectangle(self.x2,self.y2,self.x2+self.w2,self.y2+self.h2,fill=c)
        canvas.create_rectangle(self.x3,self.y3,self.x3+self.w3,self.y3+self.h3,fill=c)
        self.growButton.draw(canvas)

####################################
# Move Block Class
####################################

class MoveBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 350
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "seagreen2"
        self.direction = ""
        self.pixels = 0
        self.figure = None
        self.selectFigureBox = DropBox(self.x+50, self.y+self.margin,100,self.height//2,figures,"Figure")
        dirOptions = ["Up","Down","Left","Right"]
        self.selectDirectionBox = DropBox(self.x+160, self.y+self.margin,70,self.height//2, dirOptions,"Direction")
        self.selectPixelsBox = TextBox(self.x+240, self.y+self.margin,60,self.height//2,"Number")
        self.textBoxes = [self.selectFigureBox,self.selectDirectionBox,self.selectPixelsBox]

    def run(figure,direction,pixels):
        figure.runMove(direction,pixels)

    def moveTextbox(self):
    #adjusts the textboxes to move with the block 
        self.selectFigureBox.x = self.x + 50
        self.selectFigureBox.y = self.y + self.margin
        self.selectDirectionBox.x = self.x + 160
        self.selectDirectionBox.y = self.y + self.margin
        self.selectPixelsBox.x = self.x + 240
        self.selectPixelsBox.y = self.y + self.margin

    def typeParams(self,keysym):
    #if a textbox was clicked, type in it
        if self.selectPixelsBox.allowChange:
            self.selectPixelsBox.type(keysym)

    def updateParams(self,figures):
    #updates the objects properties based on the blocks parameters
        self.direction = self.selectDirectionBox.text
        try: self.pixels = int(self.selectPixelsBox.text)//(self.height//10)
        except: pass
        self.figure = self.selectFigureBox.text
        for figure in figures:
            if figure == self.selectFigureBox.text:
                self.figure = figure

    def draw(self,canvas,canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        canvas.create_text(self.x+10, self.y+self.height//2, text = "Move", anchor=W)
        self.selectFigureBox.draw(canvas)
        self.selectDirectionBox.draw(canvas)
        self.selectPixelsBox.draw(canvas)
        canvas.create_text(self.x+310,self.y+self.height//2,text = "pixels", anchor=W)

m = MoveBlock(4,4,[])