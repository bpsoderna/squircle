from tkinter import *
from class_dropBox import *
from class_textbox import *
from class_block import *

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
        #print("   setting",self.name, "to",self.value)
        #print("  ",type(self.name))
        for variable in data.runVariables:
            #print("    ",variable,self.name==variable)
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