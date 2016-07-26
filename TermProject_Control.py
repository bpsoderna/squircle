from tkinter import *
from class_block import *
from class_trashcan import *
from TermProject_Model import *
import pickle

def rightMousePressed(event, data):
#add blocks/figures, move individually clicked blocks/figures, resize canvas
    data.xClick, data.yClick = event.x, event.y
    if not data.displayScreen:
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
#help menu | screen | main menu
    data.xClick, data.yClick = event.x, event.y
    if data.displayHelpScreen: animateHelpScreen(event,data)
    elif data.displayScreen:
        #close screen, reset blocks/figures/variables
        if data.exitScreen.wasClicked(event.x,event.y):
            data.displayScreen = False
            data.isRunning = False
            Figure.copyFigures(data)
            for block in data.blocks:
                block.updateParams(data)
                block.reset(data.codetrashcan,data.blocks,data.variables)
    elif not data.displayScreen:
        #add blocks/figures, move connected blocks/figures, resize canvas
        clickedButton(event,data)
        connectBlocks(event,data)
        figuresAndBlocks(event,data)
        UIButtonsClicked(event,data)
        scrollButtonsClicked(event,data)
        if event.x-5<=data.codeWidth+5<=event.x+5: data.resize = True
    
def rightMouseMoved(event,data):
#move individual blocks/figures | resize canvas
    if not data.displayScreen:
        moveBlocks(event,data)
        moveFigures(event,data)
        resizeCanvas(event,data)

def leftMouseMoved(event,data):
#move connected blocks/figures | rezize canvas
    if not data.displayScreen:
        moveBlocks(event,data)
        moveFigures(event,data)
        resizeCanvas(event,data)
       
def rightMouseReleased(event, data):
#reset blocks and figures
    resetGame(event,data)

def leftMouseReleased(event,data):
#reset blocks and figures
    resetGame(event,data)

def keyPressed(event, canvas, data):
#block/figure scrollbar scrolling | typing variables | letter key press
    if data.isRunning:
        updateKey(event,data)
    elif not data.displayScreen:
        scroll(data,event.keysym)
        for block in data.blocks:
            block.setParams(event.x,event.y)
            block.typeParams(event.keysym)
        for figure in data.figures:
            figure.typeParams(event.keysym)
        if event.keysym == "Return":
            #update params and exit textboxes
            for figure in data.figures:
                figure.updateUserParams(data)
            for block in data.blocks:
                if not block.setParams(event.x,event.y):
                    for textbox in block.textboxes: textbox.wasClicked = False
                block.updateParams(data)
 
def controlClick(event,data):
#code to make copies of blocks --> object aliasing issues
    return
    if not data.displayScreen and not data.displayHelpScreen:
        makeCopy = False
        print(data.blocks)
        for block in data.blocks:
            if block.wasClicked(event.x,event.y): makeCopy = True
        if makeCopy: data.blocks.append(block.copy())

def timerFired(data):
    pass

####################################
# Helper Functions
####################################

def animateHelpScreen(event, data):
#go through help screen once, then show all instructions
        if data.exitHelpScreen.wasClicked(event.x,event.y):
            data.displayHelpScreen = False
        elif data.tutorialIndex<data.maxTutorialIndex:
            data.tutorialIndex += 1
        elif data.tutorialIndex>=data.maxTutorialIndex:
            data.displayHelpScreen = False

def resetGame(event,data):
#called when left/right mouse released
    if not data.displayScreen and not data.displayHelpScreen:
        data.resize = False
        resetBlocks(data)
        snapToGrid(data)
        deleteUnusedBlocks(event,data)
        data.newBlock = False
        resetfigures(data)
        deleteUnusedfigures(event,data)
        data.newfigure = False

def updateKey(event,data):
#called in keypress when data.isRunning
    oldKey = data.key
    data.key = event.keysym
    if oldKey != data.key:
        for block in data.queue:
            block.setTarget()

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

####################################
# Button Interactions
####################################

def clickedButton(event, data): 
#if a button is clicked, add a block/figure
    for button in data.horizontalButtons:
        if button.wasClicked(event.x,event.y):
            if button.type == "help":
                data.displayHelpScreen = True
            else:
                button.createBlock(data,event.x)
                data.newBlock = True
    for button in data.verticalButtons:
        if button.wasClicked(event.x,event.y):
            button.createfigure(data.figures,data.propertyBoxBounds,data)
            data.newfigure = True
            Figure.copyFigures(data)

def UIButtonsClicked(event,data):
#User Interface Buttons
    #Go
    if data.UIButtons[0].wasClicked(event.x,event.y):
        data.displayScreen = False
        data.isRunning = False
        Figure.copyFigures(data)
        for block in data.blocks:
            block.updateParams(data)
            block.reset(data.codetrashcan,data.blocks,data.variables)
        createQueue(data)
        data.isRunning = True
        data.displayScreen = True
    #Save
    if data.UIButtons[1].wasClicked(event.x,event.y):
        everything = [data.blocks, data.figures, data.variables]
        saveContent = pickle.dumps(everything)
        writeFile("saved.txt",saveContent)
    #Load
    if data.UIButtons[2].wasClicked(event.x,event.y):
        contentsRead = readFile("saved.txt")
        everything = pickle.loads(contentsRead)
        [data.blocks, data.figures, data.variables] = everything
    #Restart
    if data.UIButtons[3].wasClicked(event.x,event.y):
        init(data)
        data.displayHelpScreen = False
        data.tutorialIndex = data.maxTutorialIndex
    #Chase Game
    if data.UIButtons[4].wasClicked(event.x,event.y):
        contentsRead = readFile("chasegame.txt")
        everything = pickle.loads(contentsRead)
        [data.blocks, data.figures, data.variables] = everything

def scrollButtonsClicked(event,data):
#pan all blocks on code canvas the direction of the clicked arrow
    for button in data.scrollButtons:
        if button.wasClicked(event.x,event.y):
            if button.title == "v":
                for block in data.blocks:
                    block.y -= 10
                    block.moveTextbox()
            elif button.title == ">":
                for block in data.blocks:
                    block.x -= 10
                    block.moveTextbox()
            elif button.title == "<":
                for block in data.blocks:
                    block.x += 10
                    block.moveTextbox()
            elif button.title == "^":
                for block in data.blocks:
                    block.y += 10
                    block.moveTextbox()

def deleteUnusedBlocks(event,data): 
#deletes blocks not dragged onto canvas
    for button in data.horizontalButtons:
        if button.wasClicked(event.x,event.y) and abs(data.xClick-event.x) < 30 and abs(data.yClick-event.y) < 30:
            if len(data.blocks) > 1:
                data.blocks.pop()

def deleteUnusedfigures(event,data): 
#deletes figures not dragged onto canvas
    for button in data.verticalButtons:
        if button.wasClicked(event.x,event.y) and abs(data.xClick-event.x) < 30 and abs(data.yClick-event.y) < 30:
            data.figures.pop()

#copied from course notes file IO and edited
def readFile(path):
    with open(path,"rb") as f:
        return f.read()

#copied from course notes file IO and edited
def writeFile(path,contents):
    with open(path,"wb") as f:
        f.write(contents)

def resizeCanvas(event,data):
#change ratio of block:figure canvases between a min and max
    if data.resize:
        buttons = buttonWidthSum(data) + data.margin*((len(data.horizontalButtons))+2)
        stop = min(buttons,data.width-323)
        if 148 < event.x < stop:
            data.codeWidth = event.x
            updateBounds(data)

def updateBounds(data):
#updates data variables which dictate object positions relative to new codeWidth
    data.maxHStop = min(data.codeWidth, data.codeWidth - ((len(data.horizontalButtons)+1)*data.margin + buttonWidthSum(data)))
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
    addVerticalButtonLocs(data,True)
    for button in data.UIButtons:
        button.x = data.codeWidth + 2*data.margin + data.sbHeight
    for figure in data.figureCopies:
        if figure.color == "gold":
            figure.x = data.canvasBounds[0] - data.screenBounds[0] + 20

##########################
# Motion
##########################

def connectBlocks(event,data): 
#'selects' and 'connects' blocks
    resetBlocks(data)
    if not data.newBlock:
        for block in data.blocks:
            block.connect(event.x, event.y,data.blocks)

def figuresAndBlocks(event,data):
#setup all figures/blocks to be moved
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
            block.setParams(event.x,event.y)
            block.updateParams(data)
            block.grow(event.x, event.y)
    #block motion
    for block in reversed(data.blocks):
        block.selectIndividual(event.x, event.y)
        if block.drag and block.type != "start" : 
            data.blocks.remove(block)
            data.blocks.append(block)

def moveBlocks(event,data):
#moves blocks connected to clicked block, pans others
    clickedBlock = None
    for block in data.blocks:
        clickedBlock = block.moveConnected(event.x,event.y,clickedBlock,281)
    for block in data.blocks:
        block.panScreen(event,data.codeCanvasBounds,clickedBlock,data.newBlock)

def moveFigures(event,data):
#moves figures connected to clicked figure, pans others | update figureCopies 
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

###########################
# Queue
###########################

def createQueue(data):
#creates a list of blocks to be run 
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
    #print("QUEUE:",data.queue)

def addBlocksToQueue(blocks, variables, queue, minY=None, maxY=None): 
#adds simple blocks directly and complex bloxks with a JumpBlock to the queue
    block = findNextBlock(blocks, minY, maxY)
    block.inQueue = True
    copy = block.copy()
    if type(block) in {MoveBlock, MoveTowardsBlock, BounceBlock, DisplayVariableBlock,
                       VariableInstanceBlock, VariableBlock, ChangeVariableBlock, Block,
                       BounceRandomBlock, EdgeBounceBlock,GameOverBlock}:
        queue.append(copy)
    elif type(block) in {LoopBlock, IfBlock, WhileLoopBlock, ForeverLoopBlock,
                         IfKeyPressedBlock, IfTouchingBlock, IfArrowKeyPressedBlock,
                         IfMathBlock, WhileMathLoopBlock}:
        queue.append(copy)
        copy.posTag = len(queue)-1
        loopQueue(block,queue,blocks,variables)
        copy.endTag = len(queue)-1
        queue.append(JumpBlock(copy.posTag))

def loopQueue(block, queue, blocks, variables): 
#adds blocks within complex blocks (ifs/loops) tp queue 
    while findNextBlock(blocks,block.y2,block.y3) != None:
        addBlocksToQueue(blocks,variables,queue,block.y2,block.y3)

def findNextBlock(blocks,minY=None,maxY=None):
#finds the next closest block which is connected to the start block 
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
#determines whether a block is within some start/end Y values
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
#runs the queue, called each time the timer is fired
    i = 0                                                                       #HELPFUL DEBUGGING PRINTS:
    while i < len(data.queue):                                                  #print(i, block, block.ran)
        block = data.queue[i]                                                   #if type(block) == MoveBlock: print("   ("+str(block.figure.x)+","+str(block.figure.y)+")",block.target, block.direction)                         
        if not block.ran: 
            if type(block) in {MoveBlock, MoveTowardsBlock, BounceBlock, BounceRandomBlock, 
                               EdgeBounceBlock, VariableBlock, VariableInstanceBlock, 
                               DisplayVariableBlock, ForeverLoopBlock,GameOverBlock}:
                block.run(data)
                i += 1                                                          #print()
                return
            elif type(block) == ChangeVariableBlock:
                block.run(data)
                i += 1
            elif type(block) == LoopBlock:                                      #print("   loop:",block.currentLoop,"of",block.loops)
                if block.currentLoop > block.loops: 
                    i = block.endTag+2                                          #print("END:", i, len(data.queue))
                else: i += 1
            elif type(block) in {IfBlock, IfTouchingBlock, IfMathBlock}:        #print("   loop:",block.currentLoop,"of",block.loops)
                if (block.currentLoop >= block.loops or 
                    not block.evaluate(data.runVariables)):
                    i = block.endTag+2
                else: i += 1
            elif type(block) in {WhileLoopBlock, WhileMathLoopBlock}:
                block.updateParams(data)
                if not block.evaluate(data.runVariables):
                    i = block.endTag+2
                else: i += 1
            elif type(block) in {IfKeyPressedBlock, IfArrowKeyPressedBlock}:    #print("   key:",data.key)
                if not block.evaluate(data.key):
                    i = block.endTag+2
                else: i += 1
            elif type(block) == JumpBlock:
                i = block.run(data, i)                                          #print("   jumped to",i,data.queue[i])
                data.queue[i].currentLoop += 1                                  #print("   new loop:",data.queue[i].currentLoop,data.queue[i].loops)
        else: i += 1
    data.isRunning = False
