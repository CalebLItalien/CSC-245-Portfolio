from UltimateTTTRow import *
from TTTGrid import *
from TTTRow import *
from TTTNode import *

class UltimateTTTGrid:
    def __init__(self):
        self.top = UltimateTTTRow()
        self.middle = UltimateTTTRow()
        self.bottom = UltimateTTTRow()

    def winners(self):
        winners = []
        winners.append(self.__rowWinner(self.top))
        winners.append(self.__rowWinner(self.middle))
        winners.append(self.__rowWinner(self.bottom))

        winners.append(self.__column1Winner())
        winners.append(self.__column2Winner())
        winners.append(self.__column3Winner())

        winners.append(self.__diagonalA1Winner())
        winners.append(self.__diagonalA3Winner())

        for winner in winners:
            if winner != None:
                return winner
        return None

    def getA1(self):
        return self.top.getLeft()
    
    def getA2(self):
        return self.top.getMiddle()
    
    def getA3(self):
        return self.top.getRight()
    
    def getB1(self):
        return self.middle.getLeft()

    def getB2(self):
        return self.middle.getMiddle()
    
    def getB3(self):
        return self.middle.getRight()
    
    def getC1(self):
        return self.bottom.getLeft()

    def getC2(self):
        return self.bottom.getMiddle()
    
    def getC3(self):
        return self.bottom.getRight()

    def __rowWinner(self, row):
        if row.getLeftWinner() == row.getMiddleWinner() == row.getRightWinner():
            return row.getLeftWinner()
        return None

    def __column1Winner(self):
        if self.top.getLeftWinner() == self.middle.getLeftWinner() == self.bottom.getLeftWinner():
            return self.top.getLeftWinner()
        return None
    
    def __column2Winner(self):
        if self.top.getMiddleWinner() == self.middle.getMiddleWinner() == self.bottom.getMiddleWinner():
            return self.top.getMiddleWinner()
        return None
    
    def __column3Winner(self):
        if self.top.getRightWinner() == self.middle.getRightWinner() == self.bottom.getRightWinner():
            return self.top.getRightWinner()
        return None

    def __diagonalA1Winner(self):
        if self.top.getLeftWinner() == self.middle.getMiddleWinner() == self.bottom.getRightWinner():
            return self.top.getLeftWinner()
        return None
    
    def __diagonalA3Winner(self):
        if self.top.getRightWinner() == self.middle.getMiddleWinner() == self.bottom.getLeftWinner():
            return self.top.getRightWinner()
        return None