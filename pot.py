class Pot:

    def __init__(self, players, val):
        self.__players = players
        self.__value = val
        self.__winners = []

    def getplayers(self):
        return self.__players
    
    def addvalue(self, val):
        self.__value = self.__value + val
 
    def subtractvalue(self, val):
        self.__value = self.__value - val
        if self.__value < 0:
            self.__value = 0
 
    def getvalue(self):
        return self.__value

    def setwinners(self, winners):
        self.__winners = winners

    def getwinners(self):
        return self.__winners
        