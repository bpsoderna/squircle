from tkinter import *
from class_dropBox import *
from class_complexBlock import *
from class_myBlock import *

####################################
# If Else Block Class
####################################

class IfElseBlock(ComplexBlock):

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
