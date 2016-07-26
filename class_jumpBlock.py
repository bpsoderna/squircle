from tkinter import *
from class_block import *
from class_loopBlock import *
from class_ifBlock import *
from class_ifTouchingBlock import *

####################################
# Jump Block Class
####################################

class JumpBlock(Block):

    def __init__(self,jumpTo):
        self.jumpTo = jumpTo
        self.endTag = None

    def __repr__(self):
        return "JumpBlock to " + str(self.jumpTo)

    def copy(self):
        j = self.jumpTo
        copy = JumpBlock(j)
        copy.posTag = self.posTag
        return copy

    def run(self,data,endIndex):
        #data.key = None
        for i in range(self.jumpTo,endIndex):
            #print("     resetting:", data.queue[i])
            data.queue[i].ran = False
            data.queue[i].setTarget()
            if i>self.jumpTo and type(data.queue[i]) in {LoopBlock, IfBlock, IfTouchingBlock}:
                data.queue[i].currentLoop = 0
                try: self.wasTrue = False
                except: pass
        return self.jumpTo