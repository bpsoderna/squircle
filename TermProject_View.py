from tkinter import *
from class_block import *
from class_button import *
from class_trashcan import *
from TermProject_Control import *
from TermProject_Model import *

def redrawAll(canvas, data):
    canvas.create_rectangle(-5,-5,data.width+5,data.height+5,fill="azure2",width=0)
    drawText(canvas,data)
    drawCanvas(canvas,data)
    drawScrollbar(canvas,data)
    drawTrashCan(canvas,data)
    drawfigures(canvas,data)
    canvas.create_line(data.codeWidth+5,-5,data.codeWidth+5,data.height+5,width=3)
    if data.isRunning:        
        runProgram(canvas,data)
    else:
        drawBlocks(canvas,data)

####################################
# Helper Functions
####################################

def drawBlocks(canvas,data):
    for block in data.blocks:
        block.draw(canvas,data.codeCanvasBounds,data.codetrashcan)

def drawfigures(canvas,data):
    for figure in data.figures:
        figure.draw(canvas, data.canvasBounds,data.canvasTrashcan)

def drawButtons(canvas,data):
    for button in data.verticalButtons:
        button.draw(canvas,data.codeWidth,True)
    for button in data.horizontalButtons:
        button.draw(canvas,data.codeWidth,False)

def drawScrollbar(canvas,data):
    canvas.create_rectangle(-5,data.sbY,data.codeWidth+5,data.sbY+data.sbHeight,fill="azure3",width=0)
    canvas.create_rectangle(data.sbX,-5,data.sbX2,data.height+5,fill="azure3",width=0)
    drawButtons(canvas,data)

def drawCanvas(canvas,data):
    x1,y1,x2,y2 = data.codeCanvasBounds
    canvas.create_rectangle(x1,y1,x2,y2,fill="white")
    x1,y1,x2,y2 = data.canvasBounds
    canvas.create_rectangle(x1,y1,x2,y2,fill="white")

def drawText(canvas,data):
    m1 = "Welcome to my term project!"
    m2 = "Drag blocks from the scrollbar to the canvas."
    m3 = "Connect blocks beneath the bright green 'go' square to make a program."
    m4 = "Separate connected blocks by dragging with the right mouse."
    m5 = "Use the arrow keys to see more blocks."
    m6 = "Drag unwanted blocks into the trashcan to delete them."
    m7 = "Press the Spacebar to run your program"
    canvas.create_text(data.codeWidth//2, data.margin+00, anchor=N, text=m1)
    canvas.create_text(data.codeWidth//2, data.margin+15, anchor=N, text=m2)
    canvas.create_text(data.codeWidth//2, data.margin+30, anchor=N, text=m3)
    canvas.create_text(data.codeWidth//2, data.margin+45, anchor=N, text=m4)
    canvas.create_text(data.codeWidth//2, data.margin+60, anchor=N, text=m5)
    canvas.create_text(data.codeWidth//2, data.margin+75, anchor=N, text=m6)
    canvas.create_text(data.codeWidth//2, data.margin+90, anchor=N, text=m7)
    m1 = "Here is the canvas!"
    m2 = "This scrollbar is full of Figures." 
    m3 = "control the Figures using the code on the left"
    m3 = "Use the up and down arrow keys to see more Figures."
    m4 = "Press the Escape key to clear the canvas and the code."
    m5 = "Drag unwanted Figures into the trashcan to delete them."
    m6 = "When you click a Figure its properties show up in the left hand corner"
    x = ((data.sbX+8*data.margin)+(data.propertyBoxBounds[0]-data.margin))//2
    canvas.create_text(x, data.margin+00, anchor=N, text=m1)
    canvas.create_text(x, data.margin+15, anchor=N, text=m2)
    canvas.create_text(x, data.margin+30, anchor=N, text=m3)
    canvas.create_text(x, data.margin+45, anchor=N, text=m4)
    canvas.create_text(x, data.margin+60, anchor=N, text=m5)
    canvas.create_text(x, data.margin+75, anchor=N, text=m6)

def drawTrashCan(canvas,data):
    data.codetrashcan.draw(canvas)
    data.canvasTrashcan.draw(canvas)

def runProgram(canvas, data): 
#goes through blocks connected to the go block and 'runs' each one
    #note: doesn't run offscreen programs
    xStart = data.blocks[0].x
    yStart = data.blocks[0].y
    if data.yIndex < data.height:
        drawBlocks(canvas,data)
        for block in data.blocks:
            y, h = block.y, block.height
            if y<=data.yIndex<y+h and block.overlap:
                block.running = True
                if type(block) == MoveBlock:
                    try: block.figure.runMove(block.direction,block.pixels)
                    except: pass 
                drawBlocks(canvas,data)
            else:
                block.running = False
    else: 
        data.isRunning = False