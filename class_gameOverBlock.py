from tkinter import *
from class_block import *

####################################
# Game Over Block Class
####################################

class GameOverBlock(Block):

    def __init__(self,x,y):
        self.width = 80
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "mediumpurple3"

    def copy(self):
        x = self.x
        y = self.y
        copy = GameOverBlock(x,y)
        return copy

    def run(self, data):
        self.ran = True 
        data.isRunning = False

    def draw(self,canvas,canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+10, self.y+self.height//2
        x2,y2 = x1+30,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "Game Over", anchor=W)