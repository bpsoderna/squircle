from tkinter import *
from class_textbox import *
from class_complexBlock import *

####################################
# Loop Block Class
####################################

class LoopBlock(ComplexBlock):

    def __init__(self,x,y):
        w1 = 160
        h1 = 40
        x2 = x
        y2 = y + h1
        w2 = 20
        h2 = 40
        x3 = x
        y3 = y2 + h2
        w3 = 80
        h3 = 20
        super().__init__(x,y,w1,h1,x2,y2,w2,h2,x3,y3,w3,h3)
        self.color = "mediumorchid2"
        self.growButton.color = "mediumorchid4"
        self.selectLoopsBox = TextBox(self.x+50, self.y+self.margin,60,self.h1//2,"Number")
        self.textboxes = [self.selectLoopsBox]

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

    def run(self,data):
        self.currentLoop = 0
        self.ran = True

    def moveTextbox(self):
        super().moveTextbox()
        self.selectLoopsBox.x = self.x + 50
        self.selectLoopsBox.y = self.y + self.margin

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