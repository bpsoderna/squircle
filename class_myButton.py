from tkinter import *

####################################
# Button Class
####################################

class MyButton(object):

    def __init__(self,x,y,w,h,c,t,title=""):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.type = t
        self.title=title

    def __repr__(self):
        return "button type: " + str(self.type)

    def wasClicked(self,x,y):
        return ((self.x <= x <= self.x + self.width) and
                (self.y <= y <= self.y + self.height))

    def draw(self,canvas,codeWidth=0,vertical=True):
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        if vertical == None:
            canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
            canvas.create_text(x1+self.width//2,y1+self.height//2,text=self.title)
        elif vertical: 
            canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
            if self.type in {"UI","scroll"}:
                canvas.create_text(x1+self.width//2,y1+self.height//2,text=self.title)
        elif x1<codeWidth:
            if x2 > codeWidth: x2 = codeWidth
            canvas.create_rectangle(x1,y1,x2,y2,fill=self.color)
            if x2 < codeWidth:
                canvas.create_text(x1+self.width//2,y1+self.height//2,text=self.title)

