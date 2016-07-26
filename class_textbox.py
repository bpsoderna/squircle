from class_errorbox import *
from tkinter import *
import string

def typeCharacter(s,keysym):
#adds letters to string based on keypresses
#throws an error if bad characters were typed
    if s == None: s = ""
    if keysym in string.ascii_letters:
        s += keysym
    elif keysym in string.digits:
        s += keysym
    elif keysym == "BackSpace":
        s = s[:-1]
    elif keysym == "underscore" or keysym == "underscore":
        s += "_"
    elif keysym == "Shift_R" or keysym == "Shift_L":
        pass
    elif keysym == "Return":
        s = keysym
    elif keysym == "minus":
        s += "-"
    elif keysym == "space":
        s += ""
    else:
        s = None
    return s 

#####################################
# TextBox Class
#####################################

class TextBox(object):

    def __init__(self, x, y, w, h,text="Type Here"):
        self.text = text
        self.defaultText = text
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.typeError = False
        self.typeErrorBox = ErrorBox(0,0)
        self.border = 1
        self.wasClicked = False
        self.allowChange = False

    def __repr__(self):
        return str(self.text) + "   " + str(self.defaultText)

    def copy(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        text = self.text
        copy = TextBox(x,y,w,h,text)
        copy.typeError = self.typeError
        copy.border = self.border
        copy.wasClicked = self.wasClicked
        copy.allowChange = self.allowChange
        return copy

    def clicked(self,x,y):
    #returns true if a textBox was clicked
        if self.x<x<self.x+self.width and self.y<y<self.y+self.height:
            self.wasClicked = True
        else:
            self.wasClicked = False
        return self.wasClicked

    def type(self,keysym):
    #allows the user to type using keyboard if theres not an error
        if typeCharacter(self.text,keysym) == None:
            self.typeError = True
        if typeCharacter(self.text,keysym) == "Return":
            self.allowChange = False
        else:
            self.text = typeCharacter(self.text,keysym)

    def isInBounds(self,canvasBounds): 
    #determines if the textbox has left the canvas
        x1, y1  = self.x, self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        w1, h1, w2, h2 = canvasBounds
        return x1>w1 and x2<w2 and y1>h1 and y2<h2

    def draw(self,canvas):
        canvas.tag_raise(self)
        border = 3 if self.allowChange else self.border
        canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, width=border,fill="white")
        if self.typeError:
            self.typeErrorBox.draw(canvas)
        else:
            canvas.create_text(self.x+10,self.y+self.height//2,anchor=W,text=self.text)