from tkinter import *
from class_block import *
from class_trashcan import *
from TermProject_Model import *
import pickle

def rightMousePressed(event, data):
    if not data.isRunning:
        resetBlocks(data)
        clickedButton(event,data)
        for block in reversed(data.blocks):
            block.selectIndividual(event.x, event.y)
            block.shrink(event.x, event.y)
            if block.drag: return
        for figure in reversed(data.figures):
            figure.selectIndividual(event.x, event.y,data.figures)
            if figure.drag: return
        if event.x-5<=data.codeWidth+5<=event.x+5:
            data.resize = True

def leftMousePressed(event,data):
    if not data.isRunning:
        clickedButton(event,data)
        connectBlocks(event,data)
        figuresAndBlocks(event,data)
        UIButtonsClicked(event,data)
        if event.x-5<=data.codeWidth<=event.x+5:
            data.resize = True
    if data.displayScreen:
        if data.exitScreen.wasClicked(event.x,event.y):
            data.displayScreen = False
            data.isRunning = False
            Figure.copyFigures(data)
            for block in data.blocks:
                block.updateParams(data)
                block.reset(data.codetrashcan,data.blocks)

def rightMouseMoved(event,data):
    if not data.displayScreen:
        moveBlocks(event,data)
        moveFigures(event,data)
        resizeCanvas(event,data)

def leftMouseMoved(event,data):
    if not data.displayScreen:
        moveBlocks(event,data)
        moveFigures(event,data)
        resizeCanvas(event,data)
       
def rightMouseReleased(event, data):
    if not data.isRunning:
        data.resize = False
        snapToGrid(data)
        resetBlocks(data)
        deleteUnusedBlocks(data)
        data.newBlock = False
        resetfigures(data)
        deleteUnusedfigures(data)
        data.newfigure = False

def leftMouseReleased(event,data):
    if not data.isRunning:
        data.resize = False
        resetBlocks(data)
        snapToGrid(data)
        deleteUnusedBlocks(data)
        data.newBlock = False
        resetfigures(data)
        deleteUnusedfigures(data)
        data.newfigure = False

def keyPressed(event, canvas, data):
    if data.isRunning:
        oldKey = data.key
        data.key = event.keysym
        if oldKey != data.key:
            for block in data.queue:
                block.setTarget()
    else:
        scroll(data,event.keysym)
        for block in data.blocks:
            block.setParams(event.x,event.y)
            block.typeParams(event.keysym)
        for figure in data.figures:
            figure.typeParams(event.keysym)
        if event.keysym == "Return":
            for figure in data.figures:
                figure.updateUserParams(data)
            for block in data.blocks:
                if not block.setParams(event.x,event.y):
                    for textbox in block.textboxes: textbox.wasClicked = False
                block.updateParams(data)
 
def timerFired(data):
    pass

####################################
# Helper Functions
####################################

def connectBlocks(event,data): 
#'selects' and 'connects' blocks
    resetBlocks(data)
    if not data.newBlock:
        for block in data.blocks:
            block.connect(event.x, event.y,data.blocks)

def clickedButton(event, data): 
#if a button is clicked, add a block/figure
    for button in data.horizontalButtons:
        if button.wasClicked(event.x,event.y):
            button.createBlock(data,event.x)
            data.newBlock = True
    for button in data.verticalButtons:
        if button.wasClicked(event.x,event.y):
            button.createfigure(data.figures,data.propertyBoxBounds,data)
            data.newfigure = True
            Figure.copyFigures(data)

def figuresAndBlocks(event,data):
    #figure property box textboxes
    for figure in reversed(data.figures):
        if figure.setParams(event.x, event.y):
            figure.displayPropertyBox = True
            figure.updateUserParams(data)
            break
    #figure motion
    for figure in reversed(data.figures):
        figure.selectIndividual(event.x, event.y,data.figures)
        if figure.drag: break
    #block textboxes
    for block in data.blocks:
        if not data.newBlock:
            #if not block.setParams(event.x,event.y): #if none of the blocks' textboxes were clicked 
            #    for textbox in block.textboxes: textbox.wasClicked = False
            block.setParams(event.x,event.y)
            block.updateParams(data)
            block.grow(event.x, event.y)
    #block motion
    for block in reversed(data.blocks):
        block.selectIndividual(event.x, event.y)
        if block.drag and block.type != "start" : 
            data.blocks.remove(block)
            data.blocks.append(block)
            #return

def readFile(path):
    with open(path,"rb") as f:
        return f.read()

def writeFile(path,contents):
    with open(path,"wb") as f:
        f.write(contents)

def UIButtonsClicked(event,data):
    #Go
    if data.UIButtons[0].wasClicked(event.x,event.y):
        data.displayScreen = False
        data.isRunning = False
        Figure.copyFigures(data)
        for block in data.blocks:
            block.updateParams(data)
            block.reset(data.codetrashcan,data.blocks)
        createQueue(data)
        data.isRunning = True
        data.displayScreen = True
    #Save
    if data.UIButtons[1].wasClicked(event.x,event.y):
        everything = [data.blocks, data.figures]
        saveContent = pickle.dumps(everything)
        writeFile("saved.txt",saveContent)
    #Load
    if data.UIButtons[2].wasClicked(event.x,event.y):
        contentsRead = readFile("saved.txt")
        everything = pickle.loads(contentsRead)
        [data.blocks, data.figures] = everything
    #Restart
    if data.UIButtons[3].wasClicked(event.x,event.y):
        init(data)
    #Chase Game
    if data.UIButtons[4].wasClicked(event.x,event.y):
        contentsRead = readFile("chasegame.txt")
        everything = pickle.loads(contentsRead)
        [data.blocks, data.figures] = everything

def scroll(data,keysym):
#scrolls vertical and horizontal scrollbar based on arrow keys
    if keysym == "Right":
        if data.hScroll-10 >= data.maxHStop:
            data.hScroll -= 10
            data.d_hScroll = -10
            updateButtonLocs(data)
    elif keysym == "Left":
        if data.hScroll+10 <= data.minHStart:
            data.hScroll += 10
            data.d_hScroll = 10
            updateButtonLocs(data)
    elif keysym == "Down":
        if data.vScroll-10 >= data.maxVStop:
            data.vScroll -= 10
            data.d_vScroll = -10
            updateButtonLocs(data)
    elif keysym == "Up":
        if data.vScroll+10 <= data.minVStart:
            data.vScroll += 10
            data.d_vScroll = 10
            updateButtonLocs(data)

###########################
# Queue
###########################

def createQueue(data):
    data.queue = []
    minY = data.blocks[0].y
    for block in data.blocks: 
        block.inQueue = False
        block.ran = False
        block.setTarget()
    data.blocks[0].inQueue = True
    data.blocks[0].findConnected(data.blocks)
    while findNextBlock(data.blocks) != None:
        addBlocksToQueue(data.blocks,data.variables,data.queue)
    for block in data.queue:
        block.setTarget()
        block.ran = False
    print("QUEUE:",data.queue)

def addBlocksToQueue(blocks, variables, queue, minY=None, maxY=None):       
    block = findNextBlock(blocks, minY, maxY)
    block.inQueue = True
    copy = block.copy()
    if type(block) in {MoveBlock, MoveTowardsBlock, BounceBlock, DisplayVariableBlock,
                       VariableInstanceBlock, VariableBlock, ChangeVariableBlock, Block,
                       BounceRandomBlock, EdgeBounceBlock}:
        queue.append(copy)
    elif type(block) in {LoopBlock, IfBlock, WhileLoopBlock, ForeverLoopBlock,
                         IfKeyPressedBlock, IfTouchingBlock, IfArrowKeyPressedBlock}:
        queue.append(copy)
        copy.posTag = len(queue)-1
        loopQueue(block,queue,blocks,variables)
        copy.endTag = len(queue)-1                            #print("pos tag:",block, copy.posTag, "(jump to)")
        queue.append(JumpBlock(copy.posTag))

def loopQueue(block, queue, blocks, variables):
    while findNextBlock(blocks,block.y2,block.y3) != None:
        addBlocksToQueue(blocks,variables,queue,block.y2,block.y3)

def findNextBlock(blocks,minY=None,maxY=None):
    nextY = None
    nextBlock = None
    for block in blocks:
        if block.overlap and not block.inQueue:
            if nextY==None:
                if isInRange(block.y,minY,maxY):
                    nextY = block.y
                    nextBlock = block
            elif block.y<nextY:
                if isInRange(block.y,minY,maxY):
                    nextY = block.y
                    nextBlock = block
    return nextBlock

def isInRange(value, start, end):
    if start == None:
        if end == None: #start and end == None
            return True
        else: #start == None, end doesn't
            return value > end
    elif end == None: #end == None, start doesnt
        return value > start
    else: #start and end dont equal None
        return start <= value <= end

def runQueue(data):
    i = 0 
    while i < len(data.queue):
        block = data.queue[i]
        print(i, block, block.ran)                         
        #if type(block) == MoveBlock: print("   ("+str(block.figure.x)+","+str(block.figure.y)+")",block.target, block.direction)
        if not block.ran: 
            if type(block) in {MoveBlock, MoveTowardsBlock, BounceBlock, BounceRandomBlock, 
                               EdgeBounceBlock, VariableBlock, VariableInstanceBlock, 
                               DisplayVariableBlock, ForeverLoopBlock,}:
                block.run(data)
                i += 1
                print()
                return
            elif type(block) == ChangeVariableBlock:
                block.run(data)
                i += 1
            elif type(block) == LoopBlock:                     #print("   loop:",block.currentLoop,"of",block.loops)
                if block.currentLoop > block.loops: 
                    i = block.endTag+2                         #print("END:", i, len(data.queue))
                else: i += 1
            elif type(block) in {IfBlock, IfTouchingBlock}:    #print("   loop:",block.currentLoop,"of",block.loops)
                if (block.currentLoop >= block.loops or 
                    not block.evaluate(data.runVariables)):
                    i = block.endTag+2
                else: i += 1
            elif type(block) == WhileLoopBlock:
                block.updateParams(data)
                if not block.evaluate(data.runVariables):
                    i = block.endTag+2
                else: i += 1
            elif type(block) in {IfKeyPressedBlock, IfArrowKeyPressedBlock}:         #print("   key:",data.key)
                if not block.evaluate(data.key):
                    i = block.endTag+2
                else: i += 1
            elif type(block) == JumpBlock:
                i = block.run(data, i)                     #print("   jumped to",i,data.queue[i])
                data.queue[i].currentLoop += 1             #print("   new loop:",data.queue[i].currentLoop,data.queue[i].loops)
        else: i += 1
    data.isRunning = False

##########################
# Motion
##########################

def moveBlocks(event,data):
    clickedBlock = None
    for block in data.blocks:
        clickedBlock = block.moveConnected(event.x,event.y,clickedBlock,281)
    for block in data.blocks:
        block.panScreen(event,data.codeCanvasBounds,clickedBlock,data.newBlock)

def moveFigures(event,data):
    clickedfigure = None
    for figure in data.figures:
        figure.updateParams(data)
        Figure.copyFigures(data)
        copy = data.figureCopies[data.figures.index(figure)]
        dx = (data.canvasBounds[0] - data.screenBounds[0])
        dy = (data.canvasBounds[1] - data.screenBounds[1])
        clickedfigure = figure.move(event.x,event.y,clickedfigure,copy,dx,dy)
    for figure in data.figures:
        copy = data.figureCopies[data.figures.index(figure)]
        dx = (data.canvasBounds[0] - data.screenBounds[0])
        dy = (data.canvasBounds[1] - data.screenBounds[1])
        figure.panScreen(event,data.canvasBounds,clickedfigure,data.newfigure,copy,dx,dy)

def resizeCanvas(event,data):
     if data.resize:
        if 145 < event.x < data.width-323:
            data.codeWidth = event.x
            updateBounds(data)

def updateBounds(data):
    data.maxHStop = data.codeWidth - ((len(data.horizontalButtons)+1)*data.margin + buttonWidthSum(data))
    data.sbX = data.codeWidth + data.margin
    data.sbX2 = data.sbX + data.sbHeight
    canvasTop1 = data.sbY2 + data.margin
    canvasTop2 = data.height//4 + data.sbHeight//2 + data.margin
    data.codeCanvasBounds = [data.margin, canvasTop1, data.codeWidth-data.margin, data.height-data.margin]
    data.canvasBounds = [data.sbX2 + data.margin, canvasTop2, 
                        data.width-data.margin, data.height-data.margin]
    tcw = 50
    data.codetrashcan = Trashcan(tcw, data.margin, data.codeCanvasBounds)
    data.canvasTrashcan = Trashcan(tcw, data.margin, data.canvasBounds)
    addVerticalButtonLocs(data)
    for button in data.UIButtons:
        button.x = data.codeWidth + 2*data.margin + data.sbHeight