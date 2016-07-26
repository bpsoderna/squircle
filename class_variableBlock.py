from tkinter import *
from class_textbox import *
from class_block import *

####################################
# Variable Block Class
####################################

class VariableBlock(Block):

    def __init__(self,x,y,n="Variable",v="True"):
        self.width = 170
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "gold"
        self.name = n
        self.value = v
        self.nameBox = TextBox(self.x+10,self.y+10,60,20,self.name)
        self.valueBox = TextBox(self.x+100,self.y+10,60,20,self.value)
        self.textboxes = [self.nameBox, self.valueBox]
        self.display = False

    def __eq__(self,other):
        if type(other) == VariableBlock:
            return self.name == other.name # and self.value == other.value
        else: return False

    def __repr__(self):
        return str(self.name) 

    def reset(self,trashcan,blocks,variables):
    #'deselects' and 'unconnects' blocks and deletes ones in trashcan
        self.drag, self.overlap = False, False
        if self.isInTrashcan(trashcan) and self.type != "start":
            blocks.remove(self)
            variables.remove(self)

    def copy(self):
        x = self.x
        y = self.y
        n = self.nameBox
        v = self.value
        copy = VariableBlock(x,y,n,v)
        copy.width = self.width
        copy.height = self.height
        copy.margin = self.margin
        copy.color = self.color
        copy.nameBox = self.nameBox
        copy.valueBox = self.valueBox
        copy.textboxes = self.textboxes
        copy.display = self.display
        return copy

    def moveTextbox(self):
        self.nameBox.x = self.x+10
        self.nameBox.y = self.y+self.height//4
        self.valueBox.x = self.x+100
        self.valueBox.y = self.y+self.height//4

    def updateParams(self,data):
        self.name = self.nameBox.text
        self.value = self.valueBox.text
        
    def run(self,data):
        self.updateParams(data)
        if self not in data.runVariables:
            data.runVariables.append(self)
        else:
            i = data.runVariables.index(self)
            data.runVariables[i] = self
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+82,self.y+self.height//2
        x2,y2 = x1+5,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "=", anchor=W)