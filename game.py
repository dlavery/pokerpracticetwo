from blindtimer import BlindTimer
from deck import Deck
from player import Player
from hand import Hand
from card import Card
from rules import Rules
from gameexception import GameException
from gameoverexception import GameOverException

class Game:
# poker game

    __POINTS = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    __RANKING = {
        'straightflush': 9,
        'quads': 8,
        'fullhouse': 7,
        'flush': 6,
        'straight': 5,
        'trips': 4,
        'twopair': 3,
        'pair': 2,
        'highcard': 1
    }

    def __init__(self, playerlimit=8, blindinterval=600):
        self.ID = None
        self.__deck = Deck()
        self.__players = []
        self.__hands = []
        self.__inprogress = False
        self.__playerlimit = playerlimit - 1
        self.__blindtimer = BlindTimer(blindinterval)
        self.__hand = None
        self.__blinds = (0, 0)
        self.__rules = Rules()
        self.__allowedactions = ()

    def addplayer(self, player):
        # limit to 8 players
        if self.__inprogress == True:
            raise GameException('Cannot add players, game in progress')
        if len(self.__players) > self.__playerlimit:
            raise GameException('Cannot add players, game is full')
        for p in self.__players:
            if p.name() == player.name():
                raise GameException('Cannot add player, already a player with that name')
            if p.getid() == player.getid():
                raise GameException('Cannot add player, you are already registered')
        self.__players.append(player)

    def players(self):
        return self.__players

    def newhand(self):
        for player in self.__players:
            if player.getchips() <= 0:
                self.__players.remove(player)
        for player in self.__players:
            player.reset()
        self.__deck.reset()
        self.__deck.shuffle()
        self.__inprogress = True
        self.__blinds = self.__blindtimer.getblinds()
        self.__hand = Hand(self.__deck, self.__players, self.__blindtimer, self.__rules)
        self.__allowedactions = ()
        return self.__hand

    def gethand(self):
        return self.__hand

    def getblinds(self):
        return self.__blinds

    def getbigblind(self):
        return self.__blinds[1]

    def getsmallblind(self):
        return self.__blinds[0]

    def rotatedealer(self):
        if self.__players[1].getchips() <= 0:
            # don't rotate dealers if the next player is out, 
            # instead find the most recent dealer still in
            for i in range(len(self.__players)):
                player = self.__players.pop(-1)
                self.__players.insert(0, player)
                if player.getchips() > 0:
                    break
        else:
            # rotate dealers
            player = self.__players.pop(0)
            self.__players.append(player)

        # remove players from the game when they are out
        for i, player in enumerate(self.__players):
            if player.getchips() <= 0:
                del(self.__players[i])

    def getcurrentbet(self):
        return self.__hand.currentbet()

    def numberofplayers(self):
        return len(self.__players)

    def summarise(self):
        summary = {
            'in_progress': self.__inprogress,
            'big_blind': self.getbigblind(),
            'small_blind': self.getsmallblind(),
            'blind_remaining': int(round(self.__blindtimer.gettimeremaining(), 0)),
            'players': []
            }
        for player in self.__players:
            summary['players'].append(player.name())
        if self.__hand:
            summary['current_hand'] = {
                'round': self.__hand.getstatetext()
            }
        return summary
