
class PlayerHand:
# player's hand

    def __init__(self, name='unknown'):
        self.__playername = name
        self.__hand = []
        self.__ranking = 0

    def addcard(self, card):
        # receive a card
        self.__hand.append(card)

    def getplayername(self):
        return self.__playername
        
    def sethand(self, hand):
        self.__hand = hand

    def gethand(self):
        return self.__hand

    def burnhand(self):
        self.__hand = []

    def setranking(self, ranking):
        self.__ranking = ranking

    def getranking(self):
        return self.__ranking

if __name__ == "__main__":
    import unittest
    from deck import Deck
    class TestPlayerHand(unittest.TestCase):
        def setUp(self):
            pass
        def test_deal(self):
            deck = Deck()
            deck.reset()
            deck.shuffle()
            hand = PlayerHand()
            hand.addcard(deck.card())
            hand.addcard(deck.card())
            self.assertEqual(len(hand.gethand()), 2)
        def test_rank(self):
            deck = Deck()
            deck.reset()
            deck.shuffle()
            hand = PlayerHand()
            hand.addcard(deck.card())
            hand.addcard(deck.card())
            hand.addcard(deck.card())
            hand.addcard(deck.card())
            hand.addcard(deck.card())
            hand.setranking(9)
            self.assertEqual(len(hand.gethand()), 5)
            self.assertEqual(hand.getranking(), 9)
        def test_burn(self):
            deck = Deck()
            deck.reset()
            deck.shuffle()
            hand = PlayerHand()
            hand.addcard(deck.card())
            hand.addcard(deck.card())
            self.assertEqual(len(hand.gethand()), 2)
            hand.burnhand()
            self.assertEqual(len(hand.gethand()), 0)
        def test_hand(self):
            deck = Deck()
            deck.reset()
            deck.shuffle()
            cards = []
            for i in range(5):
                cards.append(deck.card())
            hand = PlayerHand()
            hand.sethand(cards)
            self.assertEqual(len(hand.gethand()), 5)
    unittest.main()