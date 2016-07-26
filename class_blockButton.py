from tkinter import *

from class_block import *
from class_complexBlock import *
from class_bounceBlock import *
from class_bounceRandomBlock import *
from class_changeVariableBlock import *
from class_commentBlock import *
from class_displayVariableBlock import *
from class_edgeBounceBlock import *
from class_foreverLoopBlock import *
from class_gameOverBlock import *
from class_ifArrowKeyPressedBlock import *
from class_ifBlock import *
from class_ifKeyPressedBlock import *
from class_ifMathBlock import *
from class_ifTouchingBlock import *
from class_jumpBlock import *
from class_loopBlock import *
from class_moveBlock import *
from class_moveTowardsBlock import *
from class_variableBlock import *
from class_variableInstanceBlock import *
from class_whileLoopBlock import *
from class_whileMathLoopBlock import *

from class_myButton import *

####################################
# Block Button Class
####################################

class BlockButton(MyButton):

    def __init__(self,x,y,w,h,c,t,title=""):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.type = t
        self.title = title

    def createBlock(self,data,click):
        x1,y1 = self.x, self.y
        w,h = self.width, self.height
        if click < data.codeWidth:
            if self.type == "move": block = MoveBlock(x1,y1,data.figures)
            elif self.type == "loop": block = LoopBlock(x1,y1)
            elif self.type == "movetowards": block = MoveTowardsBlock(x1,y1,data.figures)
            elif self.type == "edgeBounce": block = EdgeBounceBlock(x1,y1,data.figures)
            elif self.type == "instance": block= VariableInstanceBlock(x1,y1,data.variables)
            elif self.type == "if": block = IfBlock(x1,y1,data.variables)
            elif self.type == "while": block = WhileLoopBlock(x1,y1,data.variables)
            elif self.type == "forever": block = ForeverLoopBlock(x1,y1)
            elif self.type == "keypressed": block = IfKeyPressedBlock(x1,y1)
            elif self.type == "ifElse": block = IfElseBlock(x1,y1,data.variables)
            elif self.type == "displayVar": block = DisplayVariableBlock(x1,y1,data.variables)
            elif self.type == "changeVar": block = ChangeVariableBlock(x1,y1,data.variables)
            elif self.type == "bounceRandom": block = BounceRandomBlock(x1,y1,data.figures)
            elif self.type == "ifTouching": block = IfTouchingBlock(x1,y1,data.figures)
            elif self.type == "bounce": block = BounceBlock(x1,y1,data.figures)
            elif self.type == "arrowPressed": block = IfArrowKeyPressedBlock(x1,y1)
            elif self.type == "ifmath": block = IfMathBlock(x1,y1,data.variables)
            elif self.type == "gameover": block = GameOverBlock(x1,y1)
            elif self.type == "comment": block = CommentBlock(x1,y1)
            elif self.type == "whilemath": block = WhileMathLoopBlock(x1,y1,data.variables)
            elif self.type == "variable": 
                block = VariableBlock(x1,y1)
                data.variables.append(block)
            else: block = Block(x1,y1,w,h,self.color,self.type)
            data.blocks.append(block)