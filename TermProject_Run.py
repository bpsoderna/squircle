from tkinter import *

from class_block import *
from class_figure import *
from class_errorbox import *
from class_trashcan import *
from class_textbox import *
from class_button import *

from TermProject_Model import *
from TermProject_Control import *
from TermProject_View import *

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def leftMousePressedWrapper(event,canvas,data):
        leftMousePressed(event,data)
        redrawAllWrapper(canvas, data)

    def rightMousePressedWrapper(event,canvas,data):
        rightMousePressed(event,data)
        redrawAllWrapper(canvas,data)

    def leftMouseReleasedWrapper(event,canvas,data):
        leftMouseReleased(event,data)
        redrawAllWrapper(canvas, data)

    def leftMouseMovedWrapper(event,canvas,data):
        leftMouseMoved(event,data)
        #redrawAllWrapper(canvas, data)

    def rightMouseMovedWrapper(event,canvas,data):
        rightMouseMoved(event,data)
        #redrawAllWrapper(canvas, data)

    def rightMouseReleasedWrapper(event,canvas,data):
        rightMouseReleased(event,data)
        redrawAllWrapper(canvas,data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.codeWidth = data.width//2
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event: leftMousePressedWrapper(event, canvas, data))
    root.bind("<Button-3>", lambda event: rightMousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, data))
    root.bind("<B1-ButtonRelease>", lambda event: leftMouseReleasedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event: leftMouseMovedWrapper(event, canvas, data))
    root.bind("<B3-Motion>", lambda event: rightMouseMovedWrapper(event, canvas, data))
    root.bind("<B3-ButtonRelease>", lambda event: rightMouseReleasedWrapper(event,canvas,data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200,600)
