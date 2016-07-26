from class_textbox import *

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
                try: 
                    x2,y2, w2, h2 = self.x2, self.y2, self.w2, self.h2
                    cond2 = ((((x1>=x2) and (x1<=x2+w2)) or ((x2>=x1) and (x2<=x1+w1))) and 
                             (((y1>=y2) and (y1<=y2+h2)) or ((y2>=y1) and (y2<=y1+h1))))
                    x3,y3, w3, h3 = self.x3, self.y3, self.w3, self.h3
                    cond3 = ((((x1>=x3) and (x1<=x3+w3)) or ((x3>=x1) and (x3<=x1+w1))) and 
                             (((y1>=y3) and (y1<=y3+h3)) or ((y3>=y1) and (y3<=y1+h1))))
                except:
                    try:
                        x2,y2, w2, h2 = block.x2, block.y2, block.w2, block.h2
                        cond2 = ((((x>=x2) and (x<=x2+w2)) or ((x2>=x) and (x2<=x+w))) and 
                                 (((y>=y2) and (y<=y2+h2)) or ((y2>=y) and (y2<=y+h))))
                        x3,y3,w3,h3 = block.x3,block.y3,block.w3,block.h3
                        cond3 = ((((x>=x3) and (x<=x3+w3)) or ((x3>=x) and (x3<=x+w))) and 
                                 (((y>=y3) and (y<=y3+h3)) or ((y3>=y) and (y3<=y+h))))
                    except: 
                        cond2 = False
                        cond3 = False
                if (((((x1>=x) and (x1<=x+w)) or ((x>=x1) and (x<=x1+w1))) and 
                     (((y1>=y) and (y1<=y+h)) or ((y>=y1) and (y<=y1+h1)))) or cond2 or cond3):
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

