from tkinter import *
from class_dropBox import *
from class_textbox import *
from class_block import *

####################################
# Change Variable Block Class
####################################

class ChangeVariableBlock(Block):

    def __init__(self,x,y,variables,n="Variable",v=0):
        self.width = 185
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "gold"
        self.name = n
        self.variable = None
        self.value = v
        self.nameBox = DropBox(self.x+60,self.y+10,60,20,variables,self.name)
        self.valueBox = TextBox(self.x+150,self.y+10,25,20,self.value)
        self.textboxes = [self.nameBox, self.valueBox]

    def __eq__(self,other):
        if type(other) == ChangeVariableBlock:
            return self.x == other.x and self.y == other.y # and self.value == other.value
        else: return False

    def __repr__(self):
        return str(self.name)

    def copy(self):
        x = self.x
        y = self.y
        n = self.nameBox
        v = self.value
        copy = ChangeVariableBlock(x,y,n,v)
        copy.width = self.width
        copy.height = self.height
        copy.margin = self.margin
        copy.color = self.color
        copy.nameBox = self.nameBox
        copy.valueBox = self.valueBox
        copy.textboxes = self.textboxes
        return copy

    def moveTextbox(self):
        self.nameBox.x = self.x+60
        self.nameBox.y = self.y+self.height//4
        self.valueBox.x = self.x+150
        self.valueBox.y = self.y+self.height//4

    def updateParams(self,data):
        self.name = self.nameBox.text
        try: self.value = int(self.valueBox.text)
        except: pass
        
    def run(self,data):
        self.updateParams(data)
        for var in data.runVariables:
            if self.name == var:
                try:
                    val = int(var.value) 
                    val += int(self.value)
                    var.value = val
                    #print("  ",var, var.value)
                except: pass
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+10,self.y+self.height//2
        x2,y2 = x1+20,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "Change", anchor=W)
        x1,y1 = self.x+130,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "by", anchor=W)