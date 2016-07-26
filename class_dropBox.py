from tkinter import *
from class_textbox import *

#####################################
# DropBox Class
#####################################

class DropBox(TextBox):

    def __init__(self, x, y, w, h,options,text="Type Here"):
        super().__init__(x, y, w, h,text)
        self.options = options

    def select(self,x,y):
    #returns which option was clicked
        if self.x <= x <= self.x + self.width:
            for i in range(1,len(self.options)+1):
                if self.y + self.height*i <= y <= self.y + self.height*(i+1):
                    self.text = self.options[i-1]
                    self.wasClicked = False
                    return self.text

    def copy(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        o = self.options
        text = self.text
        copy = DropBox(x,y,w,h,o,text)
        copy.typeError = self.typeError
        copy.border = self.border
        copy.wasClicked = self.wasClicked
        copy.allowChange = self.allowChange
        return copy

    def clicked(self,x,y):
    #drops down box and allows user to select an option
        if self.wasClicked:
            result = self.select(x,y)
        return super().clicked(x,y)

    def type(self,keysym):
        pass #overwrite so user can no loger type

    def drawOptions(self,canvas):
        count = 1
        for option in self.options:
            x1 = self.x 
            y1 = self.y + self.height*count + 2
            x2 = self.x + self.width
            y2 = self.y + self.height*(count+1) + 2
            canvas.create_rectangle(x1,y1,x2,y2,fill="mint cream",width=0)
            canvas.create_text(x1+10,y1,text=option,anchor=NW)
            count += 1

    def draw(self,canvas):
        if self.wasClicked:
            self.drawOptions(canvas)
        super().draw(canvas)

    def type(self,keysym): pass