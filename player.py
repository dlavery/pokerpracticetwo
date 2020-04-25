import uuid
from stack import Stack
from rules import Rules
from playerhand import PlayerHand

class Player:
# card player

    def __init__(self, name, chipstack=5000):
        self.__name = name
        self.__id = uuid.uuid1()
        self.__chips = Stack(chipstack)
        self.reset()

    def reset(self):
        self.__hand = PlayerHand(self.__name)
        self.__totalbet = 0
        self.__active = True
        self.__smallblind = False
        self.__bigblind = False

    def setid(self, id):
        self.__id = id

    def getid(self):
        return self.__id

    def getplayerhand(self):
        return self.__hand

    def deal(self, card):
        # receive a card
        self.__hand.addcard(card)

    def hand(self):
        return self.__hand.gethand()

    def name(self):
        return self.__name

    def showhand(self):
        return [str(card.value())+'.'+card.suit() for card in self.__hand.gethand()]

    def addchips(self, chips):
        self.__chips.add(chips)

    def subtractchips(self, chips):
        self.__chips.subtract(chips)

    def getchips(self):
        return self.__chips.getvalue()

    def makebet(self, chips):
        self.__totalbet = self.__totalbet + chips
        self.subtractchips(chips)

    def smallblind(self, chips):
        self.__smallblind = True
        self.makebet(chips)

    def bigblind(self, chips):
        self.__bigblind = True
        self.makebet(chips)

    def isbigblind(self):
        return self.__bigblind

    def gettotalbet(self):
        return self.__totalbet

    def fold(self):
        self.__hand.burnhand()
        self.__active = False

    def isactive(self):
        return self.__active

    def clearbet(self):
        self.__totalbet = 0

    def makehand(self, community, rules):
        hand = community.getcards() + self.__hand.gethand()
        sortedhand = []
        for card in hand:
            card.setpoints(Rules.POINTS[card.value()])
            sortedhand.append(card)
        sortedhand = sorted(sortedhand, key=lambda card: (14 - card.points()))
        flushhand = rules.isflush(sortedhand)
        if flushhand:
            straighthand = rules.isstraight(flushhand)
            if straighthand:
                self.__hand.sethand(straighthand)
                self.__hand.setranking(Rules.RANKING['straightflush'])
                return self.__hand
            else:
                self.__hand.sethand(flushhand[0:5])
                self.__hand.setranking(Rules.RANKING['flush'])
                return self.__hand
        quadshand = rules.isquads(sortedhand)
        if quadshand:
            self.__hand.sethand(quadshand)
            self.__hand.setranking(Rules.RANKING['quads'])
            return self.__hand
        fullhousehand = rules.isfullhouse(sortedhand)
        if fullhousehand:
            self.__hand.sethand(fullhousehand)
            self.__hand.setranking(Rules.RANKING['fullhouse'])
            return self.__hand
        straighthand = rules.isstraight(sortedhand)
        if straighthand:
            self.__hand.sethand(straighthand)
            self.__hand.setranking(Rules.RANKING['straight'])
            return self.__hand
        tripshand = rules.istrips(sortedhand)
        if tripshand:
            self.__hand.sethand(tripshand)
            self.__hand.setranking(Rules.RANKING['trips'])
            return self.__hand
        twopairhand = rules.istwopair(sortedhand)
        if twopairhand:
            self.__hand.sethand(twopairhand)
            self.__hand.setranking(Rules.RANKING['twopair'])
            return self.__hand
        pairhand = rules.ispair(sortedhand)
        if pairhand:
            self.__hand.sethand(pairhand)
            self.__hand.setranking(Rules.RANKING['pair'])
            return self.__hand
        self.__hand.sethand(sortedhand[0:5])
        self.__hand.setranking(Rules.RANKING['highcard'])
        return self.__hand
