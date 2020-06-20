class Card:
# playing card

    def __init__(self, value, suit, points=0):
        self.__suit = suit
        self.__value = value
        self.__points = points

    def suit(self):
        return self.__suit

    def value(self):
        return self.__value

    def setpoints(self, points):
        self.__points = points

    def points(self):
        return self.__points

    def tup(self):
        return (self.__value, self.__suit)

    def asdict(self):
        return {'value': self.__value, 'suit': self.__suit}
