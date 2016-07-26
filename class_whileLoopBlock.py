from tkinter import *
from class_dropBox import *
from class_complexBlock import *

####################################
# While Loop Block Class
####################################

class WhileLoopBlock(ComplexBlock):

    def __init__(self,x,y,variables):
        w1 = 230
        h1 = 40
        x2 = x
        y2 = y + h1
        w2 = 20
        h2 = 40
        x3 = x
        y3 = y2 + h2
        w3 = 80
        h3 = 20
        self.v = variables
        super().__init__(x,y,w1,h1,x2,y2,w2,h2,x3,y3,w3,h3)
        self.color = "mediumorchid2"
        self.growButton.color = "mediumorchid4"
        self.name = None
        self.result = None
        self.selectVariableBox = DropBox(self.x+50, self.y+self.margin,70,self.h1//2,variables,"Select")
        o = ["True","False"]
        self.selectResultBox = DropBox(self.x+150,self.y+self.margin,70,self.h1//2,o,"Condition")
        self.textboxes = [self.selectVariableBox, self.selectResultBox]

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

    def run(self,data):
        self.currentLoop = 0
        self.ran = True

    def moveTextbox(self):
        super().moveTextbox()
        self.selectVariableBox.x = self.x + 50
        self.selectVariableBox.y = self.y + self.margin
        self.selectResultBox.x = self.x + 150
        self.selectResultBox.y = self.y + self.margin

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