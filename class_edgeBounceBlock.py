from tkinter import *
from class_dropBox import *
from class_block import *

####################################
# Edge Bounce Block Class
####################################

class EdgeBounceBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 210
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure = None
        self.selectFigureBox = DropBox(self.x+10, self.y+self.margin,100,self.height//2,figures,"Figure")
        self.textboxes = [self.selectFigureBox]
        self.direction = None

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = EdgeBounceBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.figure = self.figure
        copy.selectFigureBox = self.selectFigureBox
        return copy

    def moveTextbox(self):
        self.selectFigureBox.x = self.x + 10
        self.selectFigureBox.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure

    def run(self,data):
        self.figure.checkEdge = True
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+120,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "bounce off wall", anchor=W)
