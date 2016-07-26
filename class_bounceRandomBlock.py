from tkinter import *
from class_dropBox import *
from class_block import *
import random 
####################################
# Bounce Random Block Class
####################################

class BounceRandomBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 190
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.figure = None
        self.selectFigureBox = DropBox(self.x+60, self.y+self.margin,60,self.height//2,figures,"Figure")
        self.textboxes = [self.selectFigureBox]
        self.direction = None

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = BounceRandomBlock(x,y,f)
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
        self.selectFigureBox.x = self.x + 60
        self.selectFigureBox.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure

    def run(self,data):
        if self.figure.rx == 0 and self.figure.ry == 0:
            self.figure.rx = random.randint(5,10)*random.choice([-1,1])
            self.figure.ry = random.randint(5,10)*random.choice([-1,1])
        if self.figure.x < data.screenBounds[0] or self.figure.x+self.figure.width > data.screenBounds[2] :
            self.figure.rx = -self.figure.rx
        if self.figure.y < data.screenBounds[1] or self.figure.y+self.figure.height > data.screenBounds[3] :
            self.figure.ry = -self.figure.ry
        self.figure.x += self.figure.rx
        self.figure.y += self.figure.ry
        #print("  ",self.rx,self.ry)
        self.ran = True

    def draw(self, canvas, canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)
        x1,y1 = self.x+10,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "Move", anchor=W)
        x1,y1 = self.x+130,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "randomly", anchor=W)