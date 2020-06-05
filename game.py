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
        self.__rotate = False

    def __rotatedealer(self):
        big_blind_only = False
        if self.__players[0].isbigblind():
            # big blind must now be small blind
            if self.__players[0].getchips() <= 0:
                big_blind_only = True
        else:
            if self.__players[1].getchips() <= 0:
                big_blind_only = True
            player = self.__players.pop(0)
            self.__players.append(player)
        return big_blind_only

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

    def player(self, name):
        player = None
        for p in self.__players:
            if p.name() == name:
                player = p
                break
        return player

    def newhand(self):
        if self.__rotate:
            big_blind_only = self.__rotatedealer()
        else:
            self.__rotate = True
            big_blind_only = False
        # remove players from the game when they are out
        for i, player in enumerate(self.__players):
            if player.getchips() <= 0:
                del(self.__players[i])
        # reset remaining players, shuffle deck, check blinds and start a new hand
        for player in self.__players:
            player.reset()
        self.__deck.reset()
        self.__deck.shuffle()
        self.__inprogress = True
        self.__blinds = self.__blindtimer.getblinds()
        self.__hand = Hand(self.__deck, self.__players, self.__blindtimer, self.__rules, big_blind_only)
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

    def getcurrentbet(self):
        return self.__hand.currentbet()

    def numberofplayers(self):
        return len(self.__players)

    def summarise(self):
        summary = {
            'in_progress': self.__inprogress,
            'big_blind': self.getbigblind(),
            'small_blind': self.getsmallblind(),
            'blind_remaining': int(round(self.__blindtimer.gettimeremaining(), 0))
            }
        summary['players'] = [{ 'name': player.name()} for player in self.__players if player.getchips() == 0]
        if len(summary['players'] == 1):
            summary['winner'] = summary['players'][0]['name']
        if self.__hand:
            summary['current_hand'] = {
                'round': self.__hand.getstatetext()
            }
            fp = self.__hand.getfirsttoact()
            if fp:
                summary['current_hand']['first_player'] = fp.name()
            else:
                summary['current_hand']['first_player'] = ''
            lp = self.__hand.getlasttoact()
            if lp:
                summary['current_hand']['last_player'] = lp.name()
            else:
                summary['current_hand']['last_player'] = ''
            summary['current_hand']['current_player'] = {}
            (cp, options) = self.__hand.nexttobet()
            if cp:
                summary['current_hand']['current_player']['name'] = cp.name()
                summary['current_hand']['current_player']['options'] = options
                summary['current_hand']['done'] = "N"
            else:
                summary['current_hand']['done'] = "Y"
        return summary
