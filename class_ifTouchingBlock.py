from tkinter import *
from class_dropBox import *
from class_complexBlock import *

####################################
# If Touching Block Class
####################################

class IfTouchingBlock(ComplexBlock):

    def __init__(self,x,y,figures):
        self.f = figures
        w1 = 240
        h1 = 40
        x2 = x
        y2 = y + h1
        w2 = 20
        h2 = 40
        x3 = x
        y3 = y2 + h2
        w3 = 80
        h3 = 20
        super().__init__(x,y,w1,h1,x2,y2,w2,h2,x3,y3,w3,h3)
        self.color = "indianred1"
        self.growButton.color = "indianred4"
        self.name = None
        self.variableBlock = None
        self.figure1 = None
        self.figure2 = None
        self.selectFigure1Box = DropBox(self.x+30, self.y+self.margin,60,self.height//2,figures,"Figure 1")
        self.selectFigure2Box = DropBox(self.x+170, self.y+self.margin,60,self.height//2,figures,"Figure 2")
        self.textboxes = [self.selectFigure1Box, self.selectFigure2Box]
        self.wasTrue = False

    def copy(self):
        x = self.x
        y = self.y
        f = self.f
        copy = IfTouchingBlock(x,y,f)
        copy.color = self.color
        copy.x2 = self.x2
        copy.y2 = self.y2
        copy.w2 = self.w2
        copy.h2 = self.h2
        copy.x3 = self.x3
        copy.y3 = self.y3
        copy.w3 = self.w3
        copy.h3 = self.h3
        copy.name = self.name
        copy.figure1 = self.figure1
        copy.figure2 = self.figure2
        copy.selectFigure1Box = self.selectFigure1Box
        copy.selectFigure2Box = self.selectFigure2Box
        copy.textboxes = self.textboxes
        copy.growButton = self.growButton
        copy.currentLoop = self.currentLoop
        copy.loops = self.loops
        copy.wasTrue = self.wasTrue
        return copy

    def moveTextbox(self):
        super().moveTextbox()
        self.selectFigure1Box.x = self.x + 30
        self.selectFigure1Box.y = self.y + self.margin
        self.selectFigure2Box.x = self.x + 170
        self.selectFigure2Box.y = self.y + self.margin

    def updateParams(self,data):
        for figure in data.figureCopies:
            if figure == self.selectFigure1Box.text:
                self.figure1 = figure
            elif figure == self.selectFigure2Box.text:
                self.figure2 = figure

    def evaluate(self,variables):
        self.currentLoop += 1
        #print("   evaluating",self.figure1, "touching", self.figure2, ":", end=" ")
        a1,b1,c1,d1 = self.figure1.x, self.figure1.y, self.figure1.x + self.figure1.width, self.figure1.y + self.figure1.height
        a2,b2,c2,d2 = self.figure2.x, self.figure2.y, self.figure2.x + self.figure2.width, self.figure2.y + self.figure2.height
        one = b1<b2<d1
        two = a1<a2<c1
        three = b1<d2<d1
        four = a2<a1<c2
        #print((one and (two or four)) or (three and (two or four)), end = " ")
        if (one and (two or four)) or (three and (two or four)):
            #print(self.wasTrue, "-->", not self.wasTrue)
            self.wasTrue = not self.wasTrue
            return self.wasTrue
        else:
            self.wasTrue = False
            #print()
            return False

    def draw(self,canvas,canvasBounds,trashcan):
        c = super().draw(canvas,canvasBounds,trashcan)
        x1,y1 = self.x+self.margin, self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1, text = "If", anchor=W)
        x1,y1 = self.x+100,self.y+self.height//2
        x2,y2 = x1+10,y1+10
        if Block.isInBounds(x1,y1,x2,y2,canvasBounds):
            canvas.create_text(x1,y1,text="is touching", anchor=W)