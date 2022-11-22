from TTTRow import *
from TTTNode import *

## Graphs are represented A-C, 1-3, with A1 being the top left corner

class TTTGrid:
    def __init__(self):
        self.top = TTTRow() 
        self.middle = TTTRow()
        self.bottom = TTTRow()
    
    def winner(self):
        winners = []

        leftColumn = self.__getColumn(self.top.getLeft())
        middleColumn = self.__getColumn(self.top.getMiddle())
        rightColumn = self.__getColumn(self.top.getRight())

        A1Diagonal = self.__getDiagonalA1(self.top.getLeft())
        A3Diagonal = self.__getDiagonalA3(self.top.getRight())

        winners.append(self.__rowWinner(self.top))
        winners.append(self.__rowWinner(self.middle))
        winners.append(self.__rowWinner(self.bottom))

        winners.append(self.__valuesSame(leftColumn))
        winners.append(self.__valuesSame(middleColumn))
        winners.append(self.__valuesSame(rightColumn))

        winners.append(self.__valuesSame(A1Diagonal))
        winners.append(self.__valuesSame(A3Diagonal))

        for winner in winners:
            if winner != None:
                return winner
        return None        

    def setA1(self, newData):
        self.top.getLeft().setData(newData)

    def setA2(self, newData):
        self.top.getMiddle().setData(newData)

    def setA3(self, newData):
        self.top.getRight().setData(newData)

    def setB1(self, newData):
        self.middle.getLeft().setData(newData)

    def setB2(self, newData):
        self.middle.getMiddle().setData(newData)

    def setB3(self, newData):
        self.middle.getRight().setData(newData)

    def setC1(self, newData):
        self.bottom.getLeft().setData(newData)

    def setC2(self, newData):
        self.bottom.getMiddle().setData(newData)

    def setC3(self, newData):
        self.bottom.getRight().setData(newData)

    def render(self):
        

    def __rowWinner(self, row):
        if row.getRightData() == row.getMiddleData() == row.getLeftData():
            return row.getRightData()
        return None

    def __valuesSame(self, values):
        if values[0].getData() == values[1].getData() == values[2].getDAta():
            return values[0].getData()
        return None

    def __getColumn(self, startingNode):
        column = []
        column.append(startingNode)
        column.append(startingNode.getDown())
        column.append(startingNode.getDown().getDown())
        return column

    def __getDiagonalA1(self, A1):
        diagonal = []
        diagonal.append(A1)
        B1 = A1.getDown
        B2 = B1.getRight
        C2 = B2.getDown
        diagonal.append(B2)
        diagonal.append(C2.getRight)

    def __getDiagonalA3(self, A3):
        diagonal = []
        diagonal.append(A3)
        B3 = A3.getDown
        B2 = B3.getLeft
        C2 = B2.getDown
        diagonal.append(B2)
        diagonal.append(C2.getLeft)