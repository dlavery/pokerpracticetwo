from random import randint
from card import Card

class Deck:
# standard 52 playing card deck
    __SUITS = ['C', 'D', 'H', 'S']
    __VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = []
        for suit in self.__SUITS:
            for value in self.__VALUES:
                self.deck.append(Card(value, suit))

    def show(self):
        # show the deck
        for card in self.deck:
            print(str(card.show))

    def shuffle(self):
        # shuffle the deck
        temp = []
        i = 52
        while i > 0:
            i = i - 1
            temp.append(self.deck.pop(randint(0, i)))
        self.deck = temp

    def card(self):
        # return the top card
        return self.deck.pop(0)

    def size(self):
        return len(self.deck)

if __name__ == "__main__":
    import unittest
    class TestStack(unittest.TestCase):
        def setUp(self):
            pass
        def test_create(self):
            deck = Deck()
            deck.shuffle()
            self.assertEqual(deck.size(), 52)
        def test_unique(self):
            deck = Deck()
            deck.shuffle()
            cards = []
            for i in range(deck.size()):
                c = deck.card()
                card = c.value()+c.suit()
                self.assertNotIn(card, cards)
                cards.append(card)
    unittest.main()