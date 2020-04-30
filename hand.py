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

    def __init__(self, deck, players, blindtimer, rules):
        self.__deck = deck
        self.__players = players
        self.__blinds = blindtimer.getblinds()
        self.__blindtimer = blindtimer
        self.__pots = [Pot(players, 0)]
        self.__community = Community()
        self.__rules = rules
        self.__nextplayer = -1
        self.__nextplayeractions = ()
        self.__firsttoact = None

    def __setstate(self, round):
        self.__round = round
        if self.__round > self.PREFLOP:
            self.__updatepot()
        for player in self.__players:
            player.clearbet()
        if self.__round == self.PREFLOP:
            self.__players[0].smallblind(self.__blinds[0])
            self.__players[1].bigblind(self.__blinds[1])
            self.__currentbet = self.__blinds[1]
            if self.playersinhand() > 2:
                self.__nextplayer = 1
            else:
                self.__nextplayer = 0
        else:
            self.__currentbet = 0
            self.__nextplayer = -1
        self.__firsttoact = None

    def __updatepot(self):
        print('Round', self.__round)
        # No pots? What are you doing here?
        if len(self.__pots) == 0:
            return
        
        players = self.__players[:]
        
        # Find everyone who's all in
        allins = []
        for player in players:
            if player.isallin():
                allins.append((player.gettotalbet(), player.name(), player))
        allins.sort(key=lambda player: player[0])

        # fill the current pot and create a new side pot/pots
        last_allin = 0
        allin_count = 0
        for allin in allins:
            allin_count = allin_count + 1
            print('allin', allin_count, allin[2].name(), allin[2].gettotalbet())
            if allin[0] > last_allin:   # not already processed this all in bet
                player_count = 0
                for player in players:
                    player_count = player_count + 1
                    print('player', player_count, player.name(), player.gettotalbet())
                    if allin[0] > player.gettotalbet():
                        print('add to pot 1', player.gettotalbet(), player.name())
                        self.__pots[-1].addvalue(player.gettotalbet())
                        player.addedtopot(player.gettotalbet())
                    else:
                        print('add to pot 2',allin[0],player.name())
                        self.__pots[-1].addvalue(allin[0])
                        player.addedtopot(allin[0])
            last_allin = allin[0]
            players.remove(allin[2])
            if len(players) > 1:    # only create side pot if more than 1 player
                self.__pots.append(Pot(players, 0))
            else:
                players[0].addchips(player.gettotalbet()) # give the remaining chips back
                players = []
                break

        # fill the main pot or side pot for remaining players
        for player in players:
            if player.gettotalbet() == 0:
                continue
            print('add to pot 3', player.gettotalbet(), player.name())
            self.__pots[-1].addvalue(player.gettotalbet())
            player.addedtopot(player.gettotalbet())

        print('pot', self.__pots[-1].getvalue())
        '''
        while True:
            lowest_allin = None
            highest_bet = None
            players = self.__players[:]
            
            for player in players:
                if player.isallin() \
                and (lowest_allin == None or player.gettotalbet() < lowest_allin.gettotalbet()):
                    lowest_allin = player
                if highest_bet == None or player.gettotalbet() > highest_bet.gettotalbet():
                    highest_bet = player
            
            pot_amount = 0
            if lowest_allin:
                print(lowest_allin.name())
                pot_amount = lowest_allin.gettotalbet()
            elif highest_bet:
                print(highest_bet.name())
                pot_amount = highest_bet.gettotalbet()

            for player in players:
                if player.gettotalbet() > pot_amount:
                    self.__pots[-1].addvalue(pot_amount)
                    player.addedtopot(pot_amount)
                elif player.gettotalbet() > 0:
                    self.__pots[-1].addvalue(player.gettotalbet())
                    player.addedtopot(player.gettotalbet())
            
            if lowest_allin:
                players.remove(lowest_allin)
                if len(players) == 1 \
                and players[0].gettotalbet() > 0:   # last player gets their money back (all-in)
                    player[0].addchips(players[0].gettotalbet())
                    break
                else:
                    self.__pots.append(Pot(players, 0)) # create a side pot
            else:
                break
        '''
    
    def getsmallblind(self):
        return self.__blinds[0]
        
    def getbigblind(self):
        return self.__blinds[1]
        
    def getstate(self):
        return self.__round

    def getfirsttoact(self):
        return self.__firsttoact

    def nexttobet(self):
        if self.playersinhand() <= 1:
            return (None, None)

        self.__nextplayer = self.__nextplayer + 1
        if self.__nextplayer >= len(self.__players):
            self.__nextplayer = 0
        nextplayer = self.__players[self.__nextplayer]

        # get the next player to bet
        count = 0
        resetfirsttoact = False
        while nextplayer.can_act() == False:
            if self.__firsttoact == None or nextplayer.name() == self.__firsttoact.name():
                resetfirsttoact = True
            self.__nextplayer = self.__nextplayer + 1
            if self.__nextplayer >= len(self.__players):
                self.__nextplayer = 0
            nextplayer = self.__players[self.__nextplayer]
            count = count + 1
            if count >= len(self.__players):
                break

        if nextplayer.isactive() == False:  # can't find an active player
            return (None, None)
        if resetfirsttoact:
            self.__firsttoact = nextplayer
        
        # been all the way around and back to the start
        if self.__firsttoact != None and nextplayer.name() == self.__firsttoact.name():
            self.__nextplayeractions = ()
            return (None, None)

        # determine the actions allowed
        if nextplayer.gettotalbet() < self.__currentbet:
            self.__nextplayeractions = ('bet', 'fold')
        else:
            self.__nextplayeractions = ('check', 'bet', 'fold')
        
        return (nextplayer, self.__nextplayeractions)

    def currentbet(self):
        return self.__currentbet

    def act(self, player, action, amount=0):
        if player == None or player.name() != self.__players[self.__nextplayer].name():
            raise GameException('Player not allowed')   # unexpected player

        all_in = False
        if action == 'call':        # shortcut call action
            action = 'bet'
            amount = self.__currentbet - player.gettotalbet()
            if amount < 0:
                raise GameException('Call not allowed')
        elif action == 'raise':    # shortcut raise action
            action = 'bet'
            amount = amount - player.gettotalbet()
            if amount < 0:
                raise GameException('Negative raise not allowed')
        elif action == 'all-in':    # shortcut all-in action
            all_in = True
            action = 'bet'
            amount = player.getchips()
            player.allin()

        if action not in self.__nextplayeractions:
            raise GameException('Action not allowed')

        if self.__firsttoact == None:
            self.__firsttoact = player

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
                self.__firsttoact = player
            player.makebet(amount)
            if player.gettotalbet() > self.__currentbet:
                self.__currentbet = player.gettotalbet()
        elif action == 'fold':
            player.fold()
        else:
            pass

    def getcurrentpotvalue(self):
        return self.__pots[-1].getvalue()

    def getpots(self):
        return self.__pots

    def deal(self):
        for i in range(0, 2):
            for player in self.__players:
                player.deal(self.__deck.card())
        self.__setstate(self.PREFLOP)
        self.__firsttoact == None

    def playersinhand(self):
        playercount = 0
        for player in self.__players:
            if player.isactive():
                playercount = playercount + 1
        return playercount

    def flop(self):
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        for i in range (0, 3):
            self.__community.addcard(self.__deck.card())
        self.__setstate(self.FLOP)

    def burnandturn(self):
        self.__deck.card()                              # burn one
        self.__community.addcard(self.__deck.card())    # turn one

    def turn(self):
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        self.__setstate(self.TURN)
        self.burnandturn()

    def river(self):
        if self.playersinhand() < 2:
            raise GameOverException('Hand is won already')
        self.__setstate(self.RIVER)
        self.burnandturn()

    def getcommmunity(self):
        return self.__community

    def setcommunity(self, cardlist):
        self.__community.setcards(cardlist)

    def showdown(self):
        self.__setstate(self.SHOWDOWN)
        print('showdown 1')
        for pot in self.__pots:
            winners = []
            for player in pot.getplayers():
                if player.isactive() == False:
                    continue
                player.makehand(self.__community, self.__rules)
                if winners and player.getplayerhand().getranking() > winners[0].getplayerhand().getranking(): # pick the biggest ranking
                    winners = []
                    winners.append(player)
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
        print('showdown 2')

        self.__paywinners()
        print('showdown 3')
        winners = []
        for pot in self.__pots:
            winners = winners + pot.getwinners()
        return winners
        
    def __paywinners(self):
        for pot in self.__pots:
            the_pot = pot.getvalue()

            while the_pot > 0:
                if len(pot.getwinners()) == 0:
                    break
                for winner in pot.getwinners():
                    winner.addchips(1)
                    the_pot = the_pot - 1
                    if the_pot < 1:
                        break
