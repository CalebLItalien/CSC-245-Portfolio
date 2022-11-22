from TTTGrid import *
from TTTRow import *
from TTTNode import *

class UltimateTTTRow:
    def __init__(self):
        self.left = TTTGrid()
        self.middle = TTTGrid()
        self.right = TTTGrid()

    def getLeftWinner(self):
        return self.left.winner()
    
    def getMiddleWinner(self):
        return self.middle.winner()
    
    def getRightWinner(self):
        return self.right.winner()
    
    def getLeft(self):
        return self.left
    
    def getMiddle(self):
        return self.middle
    
    def getRight(self):
        return self.right
        