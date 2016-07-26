from tkinter import *
from class_figure import *
from class_myButton import *

####################################
# Figure Button Class
####################################

class FigureButton(MyButton):

    def __init__(self,w,h,c,t,title=""):
        self.x = 0
        self.y = 0
        self.width = w
        self.height = h
        self.color = c
        self.type = t
        self.title = title

    def createfigure(self,figures,propertyBoxBounds,data):
        x1,y1 = self.x, self.y
        w,h = self.width, self.height
        figure = Figure(x1,y1,w,h,self.color,self.type,propertyBoxBounds,data)
        figure.name += str(len(figures))
        figure.updateParams(data)
        figure.nameBox.defaultText = figure.name
        figures.append(figure)

