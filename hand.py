from gameexception import GameException
from gameoverexception import GameOverException
from community import Community
from pot import Pot
from rules import Rules

class Hand:
# poker hand

    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
    NOT_SET = -1

    __STATE_TEXT = {
        PREFLOP: 'pre-flop',
        FLOP: 'flop',
        TURN: 'turn',
        RIVER: 'river',
        SHOWDOWN: 'showdown',
        NOT_SET: 'not set'
    }

    def __init__(self, deck, players, blindtimer, rules, bigblindonly = False):
        self.__deck = deck
        self.__players = players
        self.__blinds = blindtimer.getblinds()
        self.__blindtimer = blindtimer
        self.__pots = [Pot(players, 0)]
        self.__community = Community()
        self.__rules = rules
        self.__bigblindonly = bigblindonly
        self.__currentplayer = None
        self.__nextplayeractions = ()
        self.__firsttoact = None
        self.__lasttoact = None
        self.__winners = []
        self.__round = self.NOT_SET

    def __setstate(self, round):
        self.__round = round
        self.__currentplayer = None
        if self.__round > self.PREFLOP:
            self.__updatepot()
        for player in self.__players:
            player.clearbet()
        if self.__round == self.PREFLOP:
            if self.__bigblindonly:
                self.__players[0].bigblind(self.__blinds[1])
            else:
                self.__players[0].smallblind(self.__blinds[0])
                self.__players[1].bigblind(self.__blinds[1])
            self.__currentbet = self.__blinds[1]
        else:
            self.__currentbet = 0

    # determine the first to act in each round
    def __getfirstactor(self):
        if self.__round == self.PREFLOP:
            starting_point = 0
            # first to act is to the left of big blind
            for i, player in enumerate(self.__players):
                if player.isbigblind():
                    starting_point = i + 1
                    if starting_point >= len(self.__players):
                        starting_point = 0
                    break
        else:
            # first to act is to the left of the dealer
            starting_point  = 0
        player = self.__players[starting_point]
        player_found = True
        player_index = starting_point
        while player.can_act() == False:
            player_index = player_index + 1
            if player_index >= len(self.__players):
                player_index = 0
            if player_index == starting_point:
                # been round once and back to the start
                player_found = False
                break
            player = self.__players[player_index]
        if player_found:
            return player
        else:
            return None
    
    def __updatepot(self):
        # No pots? What are you doing here?
        if len(self.__pots) == 0:
            return
        
        players = self.__pots[-1].getplayers()[:]
        
        # Find everyone who's all in
        allins = []
        for player in players:
            if player.isallin():
                allins.append((player.gettotalbet(), player.name(), player))
        allins.sort(key=lambda player: player[0])

        # Remove the biggest all-in as they're still in
        if len(allins) > 1 and allins[-1][0] > allins[-2][0]:
            allins[-1][2].reducebet(allins[-1][0] - allins[-2][0])
            allins[-1][2].notallin()
            self.__pots[-1].subtractvalue(allins[-1][0] - allins[-2][0])
            del(allins[-1])

        # fill the current pot and create a new side pot/pots
        last_allin = 0
        allin_count = 0
        for allin in allins:
            allin_count = allin_count + 1
            if allin[0] > last_allin:   # not already processed this all in bet
                for player in players:
                    if allin[0] > player.gettotalbet():
                        self.__pots[-1].addvalue(player.gettotalbet())
                        player.addedtopot(player.gettotalbet())
                    else:
                        self.__pots[-1].addvalue(allin[0])
                        player.addedtopot(allin[0])
            last_allin = allin[0]
            players.remove(allin[2])
            self.__pots.append(Pot(players, 0))

        # fill the main pot or side pot for remaining players
        for player in players:
            if player.gettotalbet() == 0:
                continue
            self.__pots[-1].addvalue(player.gettotalbet())
            player.addedtopot(player.gettotalbet())
    
    def getsmallblind(self):
        return self.__blinds[0]
        
    def getbigblind(self):
        return self.__blinds[1]
        
    def getstate(self):
        return self.__round

    def getstatetext(self):
        return self.__STATE_TEXT[self.__round]
        
    def getfirsttoact(self):
        return self.__firsttoact

    def getlasttoact(self):
        return self.__lasttoact

    def getwinners(self):
        return self.__winners

    def nexttobet(self):
        if self.getstate() == self.SHOWDOWN:
            return (None, None)

        if self.playersinhand() <= 1:
            return (None, None)

        if self.__nextplayeractions:    # make repeat calls idempotent
            return (self.__currentplayer, self.__nextplayeractions)

        if self.__currentplayer == None:
            if self.__firsttoact != None and self.__firsttoact.can_act() == True:
                nextplayer = self.__firsttoact
                self.__currentplayer = self.__firsttoact
            else:
                nextplayer = None
                self.__currentplayer = None
                return (None, None)
        else:
            first_player = self.__players.index(self.__firsttoact)
            player_index = self.__players.index(self.__currentplayer) + 1
            if player_index >= len(self.__players):
                player_index = 0
            nextplayer = self.__players[player_index]
            # get the next player to bet
            while nextplayer.can_act() == False:
                if player_index == first_player:    # gone back around and not found anyone to act
                    nextplayer = None
                    break
                player_index = player_index + 1
                if player_index >= len(self.__players):
                    player_index = 0
                nextplayer = self.__players[player_index]

            if nextplayer == None or nextplayer.isactive() == False:  # can't find an active player
                self.__currentplayer = None
                return (None, None)

            # been all the way around and back to the start
            if nextplayer.name() == self.__firsttoact.name():
                self.__currentplayer = None
                self.__nextplayeractions = ()
                return (None, None)

        # determine the actions allowed
        if nextplayer.gettotalbet() < self.__currentbet:
            self.__nextplayeractions = ('bet', 'fold')
        else:
            self.__nextplayeractions = ('check', 'bet', 'fold')
        
        self.__currentplayer = nextplayer
        return (nextplayer, self.__nextplayeractions)

    def currentbet(self):
        return self.__currentbet

    def act(self, player, action, amount=0):
        try:
            if player == None \
            or self.__players.index(player) < 0 \
            or player.name() != self.__currentplayer.name():
                raise GameException('Player not allowed')   # unexpected player
        except ValueError:
            raise GameException('Player not allowed')

        all_in = False
        if action == 'call':        # shortcut call action
            action = 'bet'
            amount = self.__currentbet - player.gettotalbet()
            if amount < 0:
                raise GameException('Call not allowed')
        elif action == 'raise':    # shortcut raise action
            if player.gettotalbet() > self.getsmallblind() \
            and self.__currentbet > self.getbigblind() \
            and self.__currentbet < (2 * self.getbigblind()):
                raise GameException("Cannot re-raise as previous bet was not full raise")
            action = 'bet'
            amount = amount - player.gettotalbet()
            if amount <= 0:
                raise GameException('Negative raise not allowed')
        elif action == 'all-in':    # shortcut all-in action
            all_in = True
            action = 'bet'
            amount = player.getchips()

        if action not in self.__nextplayeractions:
            raise GameException('Action not allowed')

        if action == 'check':
            pass
        elif action == 'bet':
            if amount > player.getchips():
                raise GameException("Can't bet more than your stack")
            newcurrentbet = player.gettotalbet() + amount
            if newcurrentbet == self.__currentbet:
                pass    # just a call
            elif amount < self.__blinds[1] and not all_in:
                raise GameException("Bet minimum is big blind")
            if newcurrentbet > self.__currentbet:
                self.__firsttoact = player  #re-open the betting if there's a raise
            player.makebet(amount)
            if player.gettotalbet() > self.__currentbet:
                self.__currentbet = player.gettotalbet()
            if player.getchips() == 0:
                player.allin()
        elif action == 'fold':
            player.fold()
        else:
            pass
        self.__lasttoact = player
        self.__nextplayeractions = ()

    def getcurrentplayer(self):
        return self.__currentplayer

    def getcurrentpotvalue(self):
        return self.__pots[-1].getvalue()

    def getpots(self):
        return self.__pots

    def getplayers(self):
        return self.__players

    def deal(self):
        for i in range(0, 2):
            for player in self.__players:
                player.deal(self.__deck.card())
        self.__setstate(self.PREFLOP)
        self.__firsttoact = self.__getfirstactor()

    def playersinhand(self):
        playercount = 0
        for player in self.__players:
            if player.isactive():
                playercount = playercount + 1
        return playercount

    def flop(self):
        if self.__round != self.PREFLOP:
            raise GameException('Hand not ready for a flop')
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        for i in range (0, 3):
            self.__community.addcard(self.__deck.card())
        self.__setstate(self.FLOP)
        self.__firsttoact = self.__getfirstactor()

    def burnandturn(self):
        self.__deck.card()                              # burn one
        self.__community.addcard(self.__deck.card())    # turn one

    def turn(self):
        if self.__round != self.FLOP:
            raise GameException('Hand not ready for a turn')
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        self.__setstate(self.TURN)
        self.burnandturn()
        self.__firsttoact = self.__getfirstactor()

    def river(self):
        if self.__round != self.TURN:
            raise GameException('Hand not ready for a river')
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        self.__setstate(self.RIVER)
        self.burnandturn()
        self.__firsttoact = self.__getfirstactor()

    def getcommmunity(self):
        return self.__community

    def setcommunity(self, cardlist):
        self.__community.setcards(cardlist)

    def showdown(self):
        self.__setstate(self.SHOWDOWN)
        for pot in self.__pots:
            if pot.getvalue() == 0:
                continue
            winners = []
            for player in pot.getplayers():
                if player.isactive() == False:
                    continue
                player.makehand(self.__community, self.__rules)
                if winners and player.getplayerhand().getranking() > winners[0].getplayerhand().getranking(): # pick the biggest ranking
                    winners = [player]
                elif winners and player.getplayerhand().getranking() < winners[0].getplayerhand().getranking():
                    pass
                else:
                    winners.append(player)
            if len(winners) > 1:    # equal rank, look for high card
                dedup = []
                i = 0
                highvalue = 0
                # look at each card in the hand to work out who has highest kicker
                while i < 5:
                    for winner in winners:
                        cards = winner.getplayerhand().gethand()
                        if cards[i].points() > highvalue:
                            dedup = []
                            dedup.append(winner)
                            highvalue = cards[i].points()
                        elif cards[i].points() == highvalue:
                            dedup.append(winner)
                    winners = dedup[:]
                    if len(winners) == 1:
                        break
                    dedup = []
                    highvalue = 0
                    i = i + 1
            
            pot.setwinners(winners)

        self.__paywinners()
        self.__winners = []
        for pot in self.__pots:
            self.__winners = self.__winners + pot.getwinners()
        return self.__winners
        
    def __paywinners(self):
        for pot in self.__pots[:]:
            if pot.getvalue() <= 0:
                self.__pots.remove(pot)

        for pot in self.__pots:
            if len(pot.getwinners()) == 0:
                continue
            the_pot = pot.getvalue()
            while the_pot > 0:
                for winner in pot.getwinners():
                    pot.payout(winner.name(), 1)
                    winner.addchips(1)
                    the_pot = the_pot - 1
                    if the_pot < 1:
                        break
