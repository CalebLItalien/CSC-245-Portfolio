from TTTNode import *

class TTTRow:
    
    def __init__(self):
        self.left = TTTNode()
        self.middle = TTTNode()
        self.right = TTTNode()
    
    def setLeft(self, newData):
        self.left.setData(newData)
    
    def setMiddle(self, newData):
        self.middle.setData(newData)

    def setRight(self, newData):
        self.right.setData(newData)

    def getLeft(self):
        return self.left

    def getMiddle(self):
        return self.middle
    
    def getRight(self):
        return self.right
    
    
