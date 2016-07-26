from tkinter import *

#####################################
# ErrorBox Class
#####################################

class ErrorBox(object):

    def __init__(self, x, y):
        self.text = "Typing Error: Only letters, numbers, dashes, and underscore characters"
        self.color = "red"
        self.x = x
        self.y = y
        self.width = len(self.text)*5.5
        self.height = 20

    def clicked(self,x,y):
        return self.x<x<self.x+self.width and self.y<y<self.y+self.height

    def draw(self,canvas):
        canvas.create_text(self.x,self.y,anchor=NW,text=self.text,fill=self.color)
        #canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height)