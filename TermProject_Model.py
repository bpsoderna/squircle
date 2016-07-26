from tkinter import *
from class_block import *
from class_button import *
from class_trashcan import *

def init(data):
    data.margin = 10
    initHorizontalSB(data)
    initVerticalSB(data)
    initCanvasAndBlocks(data)
    snapToGrid(data)

def initHorizontalSB(data):
    data.sbHeight = 60
    data.sbShift = 3
    data.sbY = data.height//4 - data.sbHeight//2
    data.sbY2 = data.sbY + data.sbHeight
    data.hScroll = 0
    data.d_hScroll = 0
    initHorizontalButtons(data)
    data.blocks = []
    data.newBlock = False

def initHorizontalButtons(data):
    w = data.sbHeight - 2*data.margin
    c0,c1,c2,c3,c4,c5,c6 = ("indianred1","goldenrod1","seagreen2","turquoise1",
                            "dodgerblue3","orchid4","palevioletred2")
    b0 = BlockButton(0,0,w,w,c0,"red")
    b00 = BlockButton(0,0,w,w,c0,"red1")
    b01 = BlockButton(0,0,w,w,c0,"red2")
    b1 = BlockButton(0,0,w,w,c1,"yellow")
    b10 = BlockButton(0,0,w,w,c1,"yellow1")
    b11 = BlockButton(0,0,w,w,c1,"yellow2")
    b2 = BlockButton(0,0,w,w,c2,"move")
    b20 = BlockButton(0,0,w,w,c2,"green1")
    b21 = BlockButton(0,0,w,w,c2,"green2")
    b3 = BlockButton(0,0,w,w,c3,"loop")
    b30 = BlockButton(0,0,w,w,c3,"teal1")
    b31 = BlockButton(0,0,w,w,c3,"teal2")
    b4 = BlockButton(0,0,w,w,c4,"blue")
    b40 = BlockButton(0,0,w,w,c4,"blue1")
    b41 = BlockButton(0,0,w,w,c4,"blue2")
    b5 = BlockButton(0,0,w,w,c5,"purple")
    b50 = BlockButton(0,0,w,w,c5,"purple1")
    b51 = BlockButton(0,0,w,w,c5,"purple2")
    b6 = BlockButton(0,0,w,w,c6,"pink")
    b60 = BlockButton(0,0,w,w,c6,"pink1")
    b61 = BlockButton(0,0,w,w,c6,"pink2")
    data.horizontalButtons = [b0,b00,b01,b1,b10,b11,b2,b20,b21,b3,b30,b31,b4,b40,b41,b5,b50,b51,b6,b60,b61]
    addHorizontalButtonLocs(data)
    data.minHStart = data.sbShift
    data.maxHStop = data.codeWidth - ((len(data.horizontalButtons)+1)*data.margin + buttonWidthSum(data))

def initVerticalSB(data):
    data.sbHeight = 60
    data.sbX = data.codeWidth + data.margin
    data.sbX2 = data.sbX + data.sbHeight
    data.vScroll = 0
    data.d_vScroll = 0
    initVerticalButtons(data)
    data.figures = []
    data.newfigure = False

def initVerticalButtons(data):
    w = data.sbHeight - 2*data.margin
    c0,c1,c2,c3,c4,c5,c6 = ("indianred1","goldenrod1","seagreen2","turquoise1",
                            "dodgerblue3","orchid4","palevioletred2")
    b0 = FigureButton(w,w,c0,"red")
    b00 = FigureButton(w,w,c0,"red")
    b01 = FigureButton(w,w,c0,"red")
    b1 = FigureButton(w,w,c1,"yellow")
    b10 = FigureButton(w,w,c1,"yellow")
    b11 = FigureButton(w,w,c1,"yellow")
    b2 = FigureButton(w,w,c2,"green")
    b20 = FigureButton(w,w,c2,"green")
    b21 = FigureButton(w,w,c2,"green")
    b3 = FigureButton(w,w,c3,"teal")
    b30 = FigureButton(w,w,c3,"teal")
    b31 = FigureButton(w,w,c3,"teal")
    b4 = FigureButton(w,w,c4,"blue")
    b40 = FigureButton(w,w,c4,"blue")
    b41 = FigureButton(w,w,c4,"blue")
    b5 = FigureButton(w,w,c5,"purple")
    b50 = FigureButton(w,w,c5,"purple")
    b51 = FigureButton(w,w,c5,"purple")
    b6 = FigureButton(w,w,c6,"pink")
    b60 = FigureButton(w,w,c6,"pink")
    b61 = FigureButton(w,w,c6,"pink")
    data.verticalButtons = [b0,b00,b01,b1,b10,b11,b2,b20,b21,b3,b30,b31,b4,b40,b41,b5,b50,b51,b6,b60,b61]
    addVerticalButtonLocs(data)
    data.minVStart = data.sbShift
    data.maxVStop = data.height - ((len(data.verticalButtons)+1)*data.margin + buttonHeightSum(data))

def initCanvasAndBlocks(data):
    #canvas vars 
    canvasTop = data.sbY2 + data.margin
    data.codeCanvasBounds = [data.margin, canvasTop, data.codeWidth-data.margin, data.height-data.margin]
    data.canvasBounds = [data.sbX2 + data.margin, canvasTop, 
                        data.width-data.margin, data.height-data.margin]
    #block vars
    w1,h1,w2,h2 = data.codeCanvasBounds
    b1 = Block(w1+data.margin,h1+data.margin,50,50,"green3","start")
    data.blocks = [b1]
    snapToGrid(data)
    #running vars
    data.isRunning = False
    data.yIndex = 0
    #trashcan vars
    tcw = 50
    data.codetrashcan = Trashcan(tcw, data.margin, data.codeCanvasBounds)
    data.canvasTrashcan = Trashcan(tcw, data.margin, data.canvasBounds)
    #property box vars
    pbw = 100
    data.propertyBoxBounds = [data.width-data.margin-pbw, data.margin, 
                        data.width-data.margin, canvasTop-data.margin]

####################################
# Helper Functions
####################################

def buttonWidthSum(data): 
#find total width of the buttons
    total = 0
    for button in data.horizontalButtons:
        total += button.width
    return total

def buttonHeightSum(data): 
#find total height of the buttons
    total = 0
    for button in data.verticalButtons:
        total += button.height
    return total

def addHorizontalButtonLocs(data): 
#add button locations to buttons
    bNum = 1
    bWidth = data.sbShift
    y = data.sbY + data.margin
    for button in data.horizontalButtons:
        x = data.margin*bNum + bWidth
        button.x = x
        button.y = y
        bNum += 1
        bWidth += button.width

def addVerticalButtonLocs(data): 
#add button locations to buttons
    bNum = 1
    bWidth = data.sbShift
    x = data.sbX + data.margin
    for button in data.verticalButtons:
        y = data.margin*bNum + bWidth
        button.x = x
        button.y = y
        bNum += 1
        bWidth += button.width

def updateButtonLocs(data):
#update buttonLoc list while scrolling
    for button in data.verticalButtons:
        button.y += data.d_vScroll
    data.d_vScroll = 0
    for button in data.horizontalButtons:
        button.x += data.d_hScroll
    data.d_hScroll = 0

def deleteUnusedBlocks(data): 
#deletes blocks not dragged onto canvas
    for block in data.blocks:
        for button in data.horizontalButtons:
            if block.x == button.x and block.y == button.y:
                data.blocks.pop(data.blocks.index(block))
                #note: could accidentally delete a panned off-screen bloc

def deleteUnusedfigures(data): 
#deletes figures not dragged onto canvas
    for figure in data.figures:
        for button in data.verticalButtons:
            if figure.x == button.x and figure.y == button.y:
                data.figures.pop(data.figures.index(figure))
                #note: could accidentally delete a panned off-screen figure

def snapToGrid(data): 
#snaps the blocks to a 10 pixel grid
    for block in data.blocks:
        block.snapToGrid()
    for figure in data.figures:
        figure.x = (figure.x)//10 *10
        figure.y = (figure.y)//10 *10

def resetBlocks(data): 
#'unconnects' and 'unselects' all blocks and deletes blocks in trashcan
    for block in data.blocks:
        block.reset(data.codetrashcan,data.blocks)

def resetfigures(data): 
#'unselects' all figures and deletes figures in trashcan
    for figure in data.figures:
        figure.reset(data.canvasTrashcan,data.figures)