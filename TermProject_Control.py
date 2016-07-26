from tkinter import *
from class_block import *
from class_button import *
from class_trashcan import *
from TermProject_Model import *

def rightMousePressed(event, data):
    if not data.isRunning:
        resetBlocks(data)
        clickedButton(event,data)
        for block in reversed(data.blocks):
            block.selectIndividual(event.x, event.y)
            if block.drag: 
                return
        for figure in reversed(data.figures):
            figure.selectIndividual(event.x, event.y)
            if figure.drag:
                return

def leftMousePressed(event,data):
    if not data.isRunning:
        clickedButton(event,data)
        connectBlocks(event,data)
        for figure in reversed(data.figures):
            figure.selectIndividual(event.x, event.y)
            if figure.drag: return
        for block in reversed(data.blocks):
            block.selectIndividual(event.x, event.y)
            block.setParams(event.x,event.y) 
            block.updateParams(data.figures)
            if block.drag: return

def rightMouseMoved(event,data):
    if not data.isRunning:
        clickedBlock = None
        for block in data.blocks:
            clickedBlock = block.moveFree(event.x,event.y,clickedBlock)
        for block in data.blocks:
            block.panScreen(event,data.codeCanvasBounds,clickedBlock,data.newBlock)
        clickedfigure = None
        for figure in data.figures:
            clickedfigure = figure.move(event.x,event.y,clickedfigure)
        for figure in data.figures:
            figure.panScreen(event,data.canvasBounds,clickedfigure,data.newfigure)

def leftMouseMoved(event,data):
    if not data.isRunning:
        clickedBlock = None
        for block in data.blocks:
            clickedBlock = block.moveConnected(event.x,event.y,clickedBlock)
        for block in data.blocks:
            block.panScreen(event,data.codeCanvasBounds,clickedBlock,data.newBlock)
        clickedfigure = None
        for figure in data.figures:
            clickedfigure = figure.move(event.x,event.y,clickedfigure)
        for figure in data.figures:
            figure.panScreen(event,data.canvasBounds,clickedfigure,data.newfigure)

def rightMouseReleased(event, data):
    if not data.isRunning:
        snapToGrid(data)
        resetBlocks(data)
        deleteUnusedBlocks(data)
        data.newBlock = False
        resetfigures(data)
        deleteUnusedfigures(data)
        data.newfigure = False

def leftMouseReleased(event,data):
    if not data.isRunning:
        resetBlocks(data)
        snapToGrid(data)
        deleteUnusedBlocks(data)
        data.newBlock = False
        resetfigures(data)
        deleteUnusedfigures(data)
        data.newfigure = False

def keyPressed(event, data):
    for block in data.blocks:
        block.typeParams(event.keysym)
    if event.keysym == "Escape":
        init(data)
    elif event.keysym == "space":
        data.yIndex = data.blocks[0].y
        data.blocks[0].findConnected(data.blocks, event.x, event.y)
        data.isRunning = True
    scroll(data,event.keysym)

def timerFired(data):
    if data.isRunning:
        data.yIndex += 10
        
####################################
# Helper Functions
####################################

def connectBlocks(event,data): 
#'selects' and 'connects' blocks
    resetBlocks(data)
    for block in data.blocks:
        block.connect(event.x, event.y,data.blocks)

def clickedButton(event, data): 
#if a button is clicked, add a block/figure
    for button in data.horizontalButtons:
        if button.wasClicked(event.x,event.y):
            button.createBlock(data)
            data.newBlock = True
    for button in data.verticalButtons:
        if button.wasClicked(event.x,event.y):
            button.createfigure(data.figures,data.propertyBoxBounds)
            data.newfigure = True

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

