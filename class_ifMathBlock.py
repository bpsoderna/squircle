from tkinter import *
from class_dropBox import *
from class_textbox import *
from class_complexBlock import *

####################################
# If Math Block Class
####################################

class IfMathBlock(ComplexBlock):

    def __init__(self,x,y,variables):
        self.variables = variables
        w1 = 220
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
        self.name = None
        self.variableBlock = None
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

    def moveTextbox(self):
        super().moveTextbox()
        self.variableBox.x = self.x + 30
        self.variableBox.y = self.y + self.margin
        self.mathBox.x = self.x + 110
        self.mathBox.y = self.y + self.margin
        self.numberBox.x = self.x + 150
        self.numberBox.y = self.y + self.margin

    def updateParams(self,data):
        self.name = self.variableBox.text
        try: self.number = int(self.numberBox.text)
        except: pass
        self.operator = self.mathBox.text

    def evaluate(self,variables):
        #self.ran = True
        for var in variables:
            if var.name == self.name.name:
                self.variableBlock = var
                try: self.variableBlock.value = int(self.variableBlock.value)
                except: pass
        #print("   ",self.variableBlock.value, self.operator, self.number, end = " : ")
        if self.operator == "=":
            return self.variableBlock.value == self.number
        elif self.operator == "<":
            return self.variableBlock.value < self.number
        elif self.operator == "<=":
            #print(self.variableBlock.value <= self.number)
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