from tkinter import *
from class_block import *
from class_trashcan import *
from TermProject_Control import *
from TermProject_Model import *

def redrawAll(canvas, data):
    drawCanvas(canvas,data)
    drawScrollbar(canvas,data)
    drawTrashCan(canvas,data)
    drawFigures(canvas,data)
    drawBlocks(canvas,data)
    drawScreen(canvas,data)
    drawHelp(canvas,data)

####################################
# Helper Functions
####################################

def drawHelp(canvas,data):
    if data.displayHelpScreen:
        canvas.create_rectangle(-5,-5,data.width+5,data.height+5,fill="azure2",width=0)
        name = "S\nQ\nU\n I\nR\nC\nL\nE"
        canvas.create_text(data.codeCanvasBounds[0]+data.margin,(data.codeCanvasBounds[1]+data.codeCanvasBounds[3])/2,
                            text=name,font="Ariel 45 bold",anchor=W,fill="white")
        data.exitHelpScreen.draw(canvas,data.codeWidth,None)
        a = "Welcome to SQUIRCLE!"
        b = "SQUIRCLE is a fun and easy way to learn how to program."
        c = "Put together blocks of code and watch your figures move before your eyes."
        d = "The left half of the screen contains all the code BLOCKS in a horizontal scrollbar."
        e = "Drag code blocks down from the scrollbar and use the arrow keys to see more."
        f = "Connect blocks beneath the Start block to make a program (hint: blocks snap up and to the left)."
        g = "Left-click-and-drag to move touching blocks together, right-click-and-drag to move an individual block."
        h = "Some blocks have textboxes to type in, and others let you select from a list."
        i = "To make Loop and If blocks bigger, left-click the small button at the bottom."
        j = "Similarly, to make them smaller, just right-click that button."
        k = "Drag FIGURES from the vertical scrollbar to the right half of the screen."
        l = "Rename and resize figures by clicking on their property box in the upper right hand corner."
        m = "Click and drag the black line in the center to resize the canvases."
        n = "Once you have a complete program, click the GO button to see it run."
        o = "Click the Chase Game button for inspiration."
        p = "Have Fun!"
        lines = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p]
        colors = ["indianred1","gold2","turquoise2","mediumorchid2","green3"]
        y = 50
        i = 0
        for line in range(data.tutorialIndex):
            y += 40
            i -= 1
            i %= len(colors)
            color = colors[i]
            canvas.create_text(data.width//2,y,text=lines[line],font="Ariel 20",fill=color)
        canvas.create_text(data.width//2,y+40,text="click to continue",fill="mediumorchid4",font="Ariel 12 bold")

def drawBlocks(canvas,data):
    for block in data.blocks:
        block.draw(canvas,data.codeCanvasBounds,data.codetrashcan)

def drawInstances(canvas,data):
    for var in data.varInstances:
        var.draw(canvas)

def drawFigures(canvas,data):
    for figure in data.figures:
        figure.draw(canvas, data.canvasBounds,data.canvasTrashcan)

def drawButtons(canvas,data):
    for button in data.verticalButtons:
        button.draw(canvas,data.codeWidth,True)
    for button in data.horizontalButtons:
        button.draw(canvas,data.codeWidth,False)
    for button in data.UIButtons:
        button.draw(canvas,data.codeWidth,True)
    for button in data.scrollButtons:
        button.draw(canvas,data.codeWidth,True)

def drawScrollbar(canvas,data):
    canvas.create_rectangle(-5,data.sbY,data.codeWidth+5,data.sbY+data.sbHeight,
                            fill="azure3",width=0)
    canvas.create_rectangle(data.sbX,-5,data.sbX2,data.height+5,fill="azure3",width=0)
    drawButtons(canvas,data)
    canvas.create_line(data.codeWidth+5,-5,data.codeWidth+5,data.height+5,width=3)

def drawCanvas(canvas,data):
    canvas.create_rectangle(-5,-5,data.width+5,data.height+5,fill="azure2",width=0)
    x1,y1,x2,y2 = data.codeCanvasBounds
    canvas.create_rectangle(x1,y1,x2,y2,fill="white")
    x1,y1,x2,y2 = data.canvasBounds
    canvas.create_rectangle(x1,y1,x2,y2,fill="white")
    name = "S\nQ\nU\n I\nR\nC\nL\nE"
    canvas.create_text(data.codeCanvasBounds[0]+data.margin,
                      (data.codeCanvasBounds[1]+data.codeCanvasBounds[3])/2,
                       text=name,font="Ariel 45 bold",anchor=W,fill="azure2")

def drawTrashCan(canvas,data):
    data.codetrashcan.draw(canvas)
    data.canvasTrashcan.draw(canvas)

def drawScreen(canvas,data):
    drawBlocks(canvas,data)
    if data.displayScreen:
        if data.isRunning: runQueue(data)
        x1,y1,x2,y2 = data.screenBounds
        canvas.create_rectangle(x1,y1,x2,y2,fill="white",width=5)
        for figure in data.figureCopies:
            figure.draw(canvas,data.screenBounds,None)
        data.exitScreen.draw(canvas,data.screenBounds)
