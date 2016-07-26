from tkinter import *
from class_dropBox import *
from class_block import *

####################################
# Move Towards Block Class
####################################

class MoveTowardsBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 320
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure1 = None
        self.figure2 = None
        self.selectFigure1Box = DropBox(self.x+50, self.y+self.margin,100,self.height//2,figures,"Figure 1")
        self.selectFigure2Box = DropBox(self.x+210, self.y+self.margin,100,self.height//2,figures,"Figure 2")
        self.textboxes = [self.selectFigure1Box, self.selectFigure2Box]

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = MoveTowardsBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.figure1 = self.figure1
        copy.figure2 = self.figure2
        copy.selectFigure1Box = self.selectFigure1Box
        copy.selectFigure2Box = self.selectFigure2Box
        return copy

    def moveTextbox(self):
        self.selectFigure1Box.x = self.x + 50
        self.selectFigure1Box.y = self.y + self.margin
        self.selectFigure2Box.x = self.x + 210
        self.selectFigure2Box.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigure1Box.text:
                self.figure1 = figure
            elif figure == self.selectFigure2Box.text:
                self.figure2 = figure

    def run(self,data):
        totalX = self.figure2.x - self.figure1.x
        totalY = self.figure2.y - self.figure1.y
        dx = totalX//10
        dy = totalY//10
        self.figure1.x += dx
        self.figure1.y += dy
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+10, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Move", anchor=W)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+160,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "towards", anchor=W)