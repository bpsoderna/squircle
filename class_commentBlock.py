from tkinter import *
from class_textbox import *
from class_block import *

####################################
# Comment Block Class
####################################

class CommentBlock(Block):

    def __init__(self,x,y):
        self.width = 300
        self.height = 40
        self.margin = 10
        super().__init__(x,y,self.width,self.height)
        self.color = "wheat2"
        self.commentBox = TextBox(self.x+10, self.y+self.margin,280,self.height//2,"Type Here")
        self.textboxes = [self.commentBox]

    def copy(self):
        x = self.x
        y = self.y
        copy = CommentBlock(x,y)
        copy.commentBox = self.commentBox
        return copy

    def moveTextbox(self):
    #adjusts the textboxes to move with the block 
        self.commentBox.x = self.x + 10
        self.commentBox.y = self.y + self.margin

    def draw(self,canvas,canvasBounds,trashcan):
        super().draw(canvas,canvasBounds,trashcan)
        for textbox in self.textboxes:
            if textbox.isInBounds(canvasBounds):
                textbox.draw(canvas)