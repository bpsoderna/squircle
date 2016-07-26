from tkinter import *
from class_dropBox import *
from class_textbox import *
from class_block import *
from class_figure import *

####################################
# Move Block Class
####################################

class MoveBlock(Block):

    def __init__(self,x,y,figures):
        self.width = 350
        self.height = 40
        self.margin = 10
        self.figures = figures
        super().__init__(x,y,self.width,self.height)
        self.color = "turquoise1"
        self.direction = ""
        self.pixels = 0
        self.figure = None
        self.selectFigureBox = DropBox(self.x+50, self.y+self.margin,100,self.height//2,figures,"Figure")
        dirOptions = ["Up","Down","Left","Right"]
        self.selectDirectionBox = DropBox(self.x+160, self.y+self.margin,70,self.height//2, dirOptions,"Direction")
        self.selectPixelsBox = TextBox(self.x+240, self.y+self.margin,60,self.height//2,"Number")
        self.textboxes = [self.selectFigureBox,self.selectDirectionBox,self.selectPixelsBox]
        self.target = 0

    def copy(self):
        x = self.x
        y = self.y
        f = self.figures
        copy = MoveBlock(x,y,f)
        copy.dx = self.dx
        copy.dy = self.dy
        copy.drag = self.drag
        copy.overlap = self.overlap
        copy.running = self.running
        copy.textboxes = self.textboxes
        copy.inQueue = self.inQueue
        copy.ran = self.ran
        copy.color = self.color
        copy.direction = self.direction
        copy.pixels = self.pixels
        copy.figure = self.figure
        copy.target = self.target
        copy.selectFigureBox = self.selectFigureBox
        copy.selectPixelsBox = self.selectPixelsBox
        copy.selectDirectionBox = self.selectDirectionBox
        copy.target = self.target
        return copy

    def moveTextbox(self):
    #adjusts the textboxes to move with the block 
        self.selectFigureBox.x = self.x + 50
        self.selectFigureBox.y = self.y + self.margin
        self.selectDirectionBox.x = self.x + 160
        self.selectDirectionBox.y = self.y + self.margin
        self.selectPixelsBox.x = self.x + 240
        self.selectPixelsBox.y = self.y + self.margin

    def updateParams(self,data):
    #updates the objects properties based on the blocks parameters
        self.direction = self.selectDirectionBox.text
        try: self.pixels = int(self.selectPixelsBox.text)
        except: pass
        self.figure = self.selectFigureBox.text
        for figure in data.figureCopies:
            if figure == self.selectFigureBox.text:
                self.figure = figure
                self.figure.direction = self.direction
        self.setTarget()

    def setTarget(self):
        if not self.ran and type(self.figure)==Figure:
            if self.direction == "Up":
                self.target = self.figure.y - self.pixels
            elif self.direction == "Down":
                self.target = self.figure.y + self.pixels
            elif self.direction == "Left":
                self.target = self.figure.x - self.pixels
            elif self.direction == "Right":
                self.target = self.figure.x + self.pixels

    def run(self, data):
        if self.direction == "Up":
            if self.figure.y > self.target: 
                delta = abs(self.target-self.figure.y) if abs(self.target-self.figure.y) < 10 else 10
                if not(self.figure.checkEdge and self.figure.y-delta<data.screenBounds[1]):
                    #self.direction = self.figure.direction = "Down"
                    #self.target = data.screenBounds[1] + (data.screenBounds[1]-self.target)
                    self.figure.runMove(self.direction, delta)
                self.figure.ry = -delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()
        elif self.direction == "Down":
            if self.figure.y < self.target: 
                delta = abs(self.target-self.figure.y) if abs(self.target-self.figure.y) < 10 else 10
                if self.figure.checkEdge and self.figure.y+self.figure.height+delta<data.screenBounds[3]:
                    self.direction = self.figure.direction = "Up"
                    self.target = data.screenBounds[3] - (self.target-data.screenBounds[3])
                self.figure.runMove(self.direction, delta)
                self.figure.ry = delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()
        elif self.direction == "Right":
            if self.figure.x < self.target: 
                delta = abs(self.target-self.figure.x) if abs(self.target-self.figure.x) < 10 else 10
                if not (self.figure.checkEdge and self.figure.x+self.figure.width+delta>data.screenBounds[2]):
                    #self.direction = self.figure.direction = "Left"
                    #self.target = data.screenBounds[2] - (self.target-data.screenBounds[2])
                    self.figure.runMove(self.direction, delta)
                self.figure.rx = delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()
        elif self.direction == "Left":
            if self.figure.x > self.target: 
                delta = abs(self.target-self.figure.x) if abs(self.target-self.figure.x) < 10 else 10
                if not (self.figure.checkEdge and self.figure.x-delta<data.screenBounds[0]):
                    #self.direction = self.figure.direction = "Right"
                    #self.target = data.screenBounds[0] + (data.screenBounds[0]-self.target)
                    self.figure.runMove(self.direction, delta)
                self.figure.rx = -delta
            else: 
                self.ran = True
                data.key = None
                for block in data.queue: block.setTarget()

    def draw(self,canvas,canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+10, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Move", anchor=W)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                #canvas.tag_raise(textbox)
                textbox.draw(canvas)
        x1,y1 = self.x+310,self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text = "pixels", anchor=W)