from tkinter import *
from class_myButton import *
from class_block import *

####################################
# Complex Block Class
####################################

class ComplexBlock(Block):

    def __init__(self,x,y,w,h,x2,y2,w2,h2,x3,y3,w3,h3):
        self.margin = 10
        super().__init__(x,y,w,h)
        self.x = x
        self.y = y
        self.w1 = w
        self.h1 = h
        self.x2 = x2
        self.y2 = y2
        self.w2 = w2
        self.h2 = h2
        self.x3 = x3
        self.y3 = y3
        self.w3 = w3
        self.h3 = h3
        self.growButton = MyButton(self.x+65,self.y+85,10,10,self.color,"grow")
        self.textboxes = []
        self.currentLoop = 0
        self.loops = 1

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

    def moveTextbox(self):
        self.x2 = self.x
        self.y2 = self.y + self.h1
        self.x3 = self.x
        self.y3 = self.y2 + self.h2
        self.growButton.x = self.x+65
        self.growButton.y = self.y+self.h1+self.h2+5 

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
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