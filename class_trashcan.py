####################################
# Trashcan Class
####################################

class Trashcan(object):

    def __init__(self,size,margin,canvasBounds):
        X1,Y1,X2,Y2 = canvasBounds
        self.x1 = X2-margin-size
        self.y1 = Y1+margin
        self.x2 = X2-margin
        self.y2 = Y1+margin+size

    def draw(self,canvas):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        canvas.create_rectangle(x1,y1,x2,y2,fill="gray")