from tkinter import *
from class_dropBox import *
from class_complexBlock import *
from class_myButton import *

####################################
# IfArrowKeyPressed Block Class
####################################

class IfArrowKeyPressedBlock(ComplexBlock):

    def __init__(self,x,y):
        w1 = 170
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
        self.color = "indianred1"
        self.growButton.color = "indianred4"
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

    def moveTextbox(self):
        super().moveTextbox()
        self.keyBox.x = self.x + 30 
        self.keyBox.y = self.y + 10

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