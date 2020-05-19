import sys
from game import Game
from player import Player
from gameexception import GameException

def do_betting(hand):
    while True:
        (actor, options) = hand.nexttobet()
        if actor == None:
            break
        if 'bet' in options:
            options = options + ('call', 'raise')
        print(actor.name(), 'to act', options ,'; pot:', hand.getpots()[-1].getvalue(), '; blinds:', hand.getsmallblind(), ',', hand.getbigblind(), '; stack:', actor.getchips(), '; current bet:', hand.currentbet())
        act_split = ('',)
        while act_split[0] not in options:
            act = input('Action?')
            act_split = act.split(' ')
            if (act_split[0] == 'bet' or act_split[0] == 'raise') and len(act_split) < 2:
                act_split = ('',)
                continue
            if len(act_split) > 1:
                try:
                    betval = int(act_split[1])
                except ValueError as e:
                    betval = 0
            else:
                betval = 0
            try:
                hand.act(actor, act_split[0], betval)
            except GameException as e:
                print(str(e))
                act_split = ('',)

def main():
    game = Game()
    game.addplayer(Player('Alice'))
    game.addplayer(Player('Bob'))
    game.addplayer(Player('Carla'))
    game.addplayer(Player('Dave'))
    gamenumber = 0
    while True:
      answ = input('Deal? (Y/n)')
      if answ == 'n' or answ == 'N':
          sys.exit(0)
      gamenumber = gamenumber + 1
      hand = game.newhand()
      hand.deal()
      print('- Hand ' + str(gamenumber))
      for player in game.players():
          print(player.name(), ':', player.showhand())
      do_betting(hand)
      if hand.playersinhand() > 1:
          answ = input('Flop? (Y/n)')
          if answ == 'n' or answ == 'N':
              sys.exit(0)
          hand.flop()
          print(hand.getcommmunity().show())
          do_betting(hand)
          if hand.playersinhand() > 1:
              answ = input('Turn? (Y/n)')
              if answ == 'n' or answ == 'N':
                  sys.exit(0)
              hand.turn()
              print(hand.getcommmunity().show())
              do_betting(hand)
              if hand.playersinhand() > 1:
                  answ = input('River? (Y/n)')
                  if answ == 'n' or answ == 'N':
                      sys.exit(0)
                  hand.river()
                  print(hand.getcommmunity().show())
                  do_betting(hand)
                  if hand.playersinhand() > 1:
                      answ = input('Showdown? (Y/n)')
                      if answ == 'n' or answ == 'N':
                          sys.exit(0)
      winners = hand.showdown()
      for w in winners:
          print(w.name(), w.showhand())
      if len(winners) == 1:
          print(winners[0].name(), 'wins', hand.getpots()[-1].getvalue(), 'chips!')
      else:
          wintext = ''
          for winner in winners:
              wintext = wintext + winner.name() + ', '
          print(wintext, 'chop', str(hand.getpots()[-1]), 'chips!')
      print('-')

if __name__ == "__main__":
    main()
