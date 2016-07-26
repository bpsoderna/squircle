from class_errorbox import *
from tkinter import *
from tkinter import font
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
        return str(self.text) + "   " + self.defaultText

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
        else:
            self.text = typeCharacter(self.text,keysym)

    def draw(self,canvas):
        border = 3 if self.wasClicked else self.border
        canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, width=border,fill="white")
        if self.typeError:
            self.typeErrorBox.draw(canvas)
        else:
            canvas.create_text(self.x+10,self.y+self.height//2,anchor=W,text=self.text)

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