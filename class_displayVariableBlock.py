from tkinter import *
from class_dropBox import *
from class_block import *
from class_variableBlock import *
from class_figure import *

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
        try:self.variable.display = True
        except: pass
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
