class Community:
# poker community cards

    def __init__(self):
        self.__cards = []

    def addcard(self, card):
        self.__cards.append(card)

    def getcards(self):
        return self.__cards

    def setcards(self, cards):
        self.__cards = cards

    def show(self):
        return [str(card.value())+'.'+card.suit() for card in self.__cards]

if __name__ == "__main__":
    import unittest
    from deck import Deck
    class TestCommunity(unittest.TestCase):
        def setUp(self):
            pass
        def test_flop(self):
            deck = Deck()
            deck.shuffle()
            community = Community()
            community.addcard(deck.card())
            community.addcard(deck.card())
            community.addcard(deck.card())
            cards = community.getcards()
            self.assertEqual(len(cards), 3)
            x = (cards[0].suit() == cards[1].suit())
            y = (cards[0].value() == cards[1].value())
            self.assertEqual((x and y), False)
        def test_turn(self):
            deck = Deck()
            deck.shuffle()
            community = Community()
            community.addcard(deck.card())
            community.addcard(deck.card())
            community.addcard(deck.card())
            community.addcard(deck.card())
            self.assertEqual(len(community.getcards()), 4)
        def test_river(self):
            deck = Deck()
            deck.shuffle()
            community = Community()
            community.addcard(deck.card())
            community.addcard(deck.card())
            community.addcard(deck.card())
            community.addcard(deck.card())
            community.addcard(deck.card())
            self.assertEqual(len(community.getcards()), 5)
        def test_overwrite(self):
            deck = Deck()
            deck.shuffle()
            cards = []
            for i in range(3):
                cards.append(deck.card())
            community = Community()
            community.setcards(cards)
            self.assertEqual(len(community.getcards()), 3)
    unittest.main()