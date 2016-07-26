from tkinter import *
from class_block import *
from class_trashcan import *

def init(data):
    data.codeWidth = data.width//2
    data.margin = 10
    initHorizontalSB(data)
    initVerticalSB(data)
    initCanvasAndBlocks(data)
    initUIButtons(data)
    snapToGrid(data)
    data.figureCopies = []
    data.resize = False
    data.key = None 

def initHorizontalSB(data):
    data.sbHeight = 60
    data.sbShift = 3
    data.sbY = data.margin #data.height//4 - data.sbHeight//2
    data.sbY2 = data.sbY + data.sbHeight
    data.hScroll = 0
    data.d_hScroll = 0
    initHorizontalButtons(data)
    data.blocks = []
    data.runVariables = []
    data.variables = []
    data.newBlock = False

def initUIButtons(data):
    x = data.codeWidth + 2*data.margin + data.sbHeight
    w = 75
    h = 35
    go = MyButton(x,h*0+data.margin*1,w,h,"powderblue","UI","Go!")
    save = MyButton(x,h*1+data.margin*2,w,h,"powderblue","UI","Save")
    load = MyButton(x,h*2+data.margin*3,w,h,"powderblue","UI","Load")
    restart = MyButton(x,h*3+data.margin*4,w,h,"powderblue","UI","Restart")
    chase = MyButton(x,h*4+data.margin*5,w,h,"powderblue","UI","Chase Game")
    data.UIButtons = [go,save,load,restart,chase]

def initHorizontalButtons(data):
    h = data.sbHeight - 2*data.margin
    w = h + 12
    c0,c1,c2,c3 = ("indianred1","gold","turquoise1","mediumorchid2")
    b0 = BlockButton(0,0,w,h,c0,"if", "if")
    b1 = BlockButton(0,0,w,h,c0,"keypressed"," key\npress")
    b2 = BlockButton(0,0,w,h,c0,"arrowPressed","arrow\npress")
    #b3 = BlockButton(0,0,w,h,c0,"ifElse","if else")
    b4 = BlockButton(0,0,w,h,c0,"ifTouching","touching\n   figure")
    b5 = BlockButton(0,0,w,h,c1,"variable","  new\nvariable")
    b6 = BlockButton(0,0,w,h,c1,"instance","   set\nvariable")
    b7 = BlockButton(0,0,w,h,c1,"displayVar","display\nvariable")
    b8 = BlockButton(0,0,w,h,c1,"changeVar"," change\nvariable")
    b9 = BlockButton(0,0,w,h,c2,"move","move")
    b10 = BlockButton(0,0,w,h,c2,"movetowards","  move\ntowards")
    b11 = BlockButton(0,0,w,h,c2,"edgeBounce","  edge\nbounce")
    b12 = BlockButton(0,0,w,h,c2,"bounceRandom","   move\nrandomly")
    #b13 = BlockButton(0,0,w,h,c2,"bounce","bounce")
    b14 = BlockButton(0,0,w,h,c3,"loop","loop")
    b15 = BlockButton(0,0,w,h,c3,"while","while\n loop")
    b16 = BlockButton(0,0,w,h,c3,"forever","forever\n  loop")
    data.horizontalButtons = [b0,b1,b2,b4,b5,b6,b7,b8,b9,b10,b11,b12,b14,b15,b16]
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
    b0 = FigureButton(w,w,"firebrick3","red")
    b1 = FigureButton(w,w,"indianred1","red")
    b2 = FigureButton(w,w,"coral","orange")
    b3 = FigureButton(w,w,"darkorange1","orange")
    b4 = FigureButton(w,w,"goldenrod1","yellow")
    b5 = FigureButton(w,w,"lightgoldenrod1","yellow")
    b6 = FigureButton(w,w,"darkolivegreen1","green")
    b7 = FigureButton(w,w,"seagreen2","green")
    b8 = FigureButton(w,w,"springgreen3","green")
    b9 = FigureButton(w,w,"forestgreen","green")
    b10 = FigureButton(w,w,"turquoise4","blue")
    b11 = FigureButton(w,w,"darkturquoise","blue")
    b12 = FigureButton(w,w,"turquoise2","blue")
    b13 = FigureButton(w,w,"deepskyblue","blue")
    b14 = FigureButton(w,w,"dodgerblue3","blue")
    b15 = FigureButton(w,w,"slateblue","blue")
    b16 = FigureButton(w,w,"mediumpurple2","purple")
    b17 = FigureButton(w,w,"darkorchid3","purple")
    b18 = FigureButton(w,w,"orchid4","purple")
    b19 = FigureButton(w,w,"hotpink4","purple")
    b20 = FigureButton(w,w,"palevioletred2","pink")
    b21 = FigureButton(w,w,"hotpink","pink")
    b22 = FigureButton(w,w,"maroon2","pink")
    data.verticalButtons = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,
                            b15,b16,b17,b18,b19,b20,b21,b22]
    addVerticalButtonLocs(data)
    data.minVStart = data.sbShift
    data.maxVStop = data.height - ((len(data.verticalButtons)+1)*data.margin + buttonHeightSum(data))

def initCanvasAndBlocks(data):
    #canvas vars 
    canvasTop1 = data.sbY2 + data.margin
    canvasTop2 = data.height//4 + data.sbHeight//2 + data.margin
    data.codeCanvasBounds = [data.margin, canvasTop1, data.codeWidth-data.margin, data.height-data.margin]
    data.canvasBounds = [data.sbX2 + data.margin, canvasTop2, 
                        data.width-data.margin, data.height-data.margin]
    #block vars
    w1,h1,w2,h2 = data.codeCanvasBounds
    b1 = Block(w1+data.margin,h1+data.margin,50,50,"green3","start","START")
    data.blocks = [b1]
    snapToGrid(data)
    #running vars
    data.isRunning = False
    data.displayScreen = False
    data.yIndex = 0
    #trashcan vars
    tcw = 50
    data.codetrashcan = Trashcan(tcw, data.margin, data.codeCanvasBounds)
    data.canvasTrashcan = Trashcan(tcw, data.margin, data.canvasBounds)
    #property box vars
    pbw = 150
    data.propertyBoxBounds = [data.width-data.margin-pbw, data.margin, 
                        data.width-data.margin, canvasTop2-data.margin-4]
    #screen vars
    width = data.canvasBounds[2] - data.canvasBounds[0]
    height = data.canvasBounds[3] - data.canvasBounds[1]
    x1 = data.width//2 - width//2
    x2 = x1 + width 
    y1 = data.height//2 - height//2
    y2 = y1 + height
    data.screenBounds = [x1,y1,x2,y2]
    data.exitScreen = MyButton(x2-20, y1+10,10,10,"red","exitScreen")

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

def resetBlocks(data): 
#'unconnects' and 'unselects' all blocks and deletes blocks in trashcan
    for block in data.blocks:
        block.reset(data.codetrashcan,data.blocks)

def resetfigures(data): 
#'unselects' all figures and deletes figures in trashcan
    for figure in data.figures:
        figure.reset(data.canvasTrashcan,data.figures,data.figureCopies)