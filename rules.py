from card import Card

class Rules:
# poker rules

    POINTS = {
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

    RANKING = {
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

    def __init__(self):
        pass

    def isquads(self, hand):
        count = {}
        quadhand = False
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k, v in count.items():
            if len(v) > 3:
                quadhand = v
                break
        if quadhand:
            for k in sorted(count, reverse=True):
                if len(count[k]) < 4:
                    quadhand.append(count[k][0])
                    break
        return quadhand

    def isfullhouse(self, hand):
        count = {}
        fhhand = False
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        sortedcount = sorted(count, reverse=True)
        for k in sortedcount:
            if len(count[k]) == 3:
                fhhand = count[k]
                break
        if fhhand:
            for k in sortedcount:
                if len(count[k]) == 2:
                    fhhand = fhhand + count[k]
                    break
        if fhhand and len(fhhand) == 5:
            return fhhand
        else:
            return False

    def isflush(self, hand):
        clubs = []
        diamonds = []
        hearts = []
        spades = []
        for card in hand:
            if card.suit() == 'C':
                clubs.append(card)
            elif card.suit() == 'D':
                diamonds.append(card)
            elif card.suit() == 'H':
                hearts.append(card)
            else:
                spades.append(card)
        # got a flush?
        if len(clubs) > 4:
            return clubs
        elif len(diamonds) > 4:
            return diamonds
        elif len(hearts) > 4:
            return hearts
        elif len(spades) > 4:
            return spades
        return False

    def isstraight(self, hand):
        topcard = hand[0]
        newhand = hand[:]
        if topcard.value() == 'A':
            # ace can be low too
            bottomcard = Card(topcard.value(), topcard.suit())
            bottomcard.setpoints(1)
            newhand.append(bottomcard)
        straight = []
        lastvalue = 0
        for card in newhand:
            if straight == [] or card.points() == (lastvalue - 1):
                straight.append(card)
            elif card.points() == lastvalue:
                continue
            else:
                straight = []
                straight.append(card)
            if len(straight) > 4:
                return straight
            lastvalue = card.points()
        return False

    def istrips(self, hand):
        count = {}
        tripshand = False
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k in sorted(count, reverse=True):
            if len(count[k]) == 3:
                tripshand = count[k]
                break
        if tripshand:
            for card in hand:
                if card not in tripshand:
                    tripshand.append(card);
                if len(tripshand) > 4:
                    break
        return tripshand

    def istwopair(self, hand):
        count = {}
        tphand = []
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k in sorted(count, reverse=True):
            if len(count[k]) == 2:
                tphand = tphand + count[k]
            if len(tphand) == 4:
                break
        if len(tphand) == 4:
            for card in hand:
                if card not in tphand:
                    tphand.append(card);
                    break
        else:
            return False
        return tphand

    def ispair(self, hand):
        count = {}
        pairhand = []
        for card in hand:
            if card.points() not in count:
                count[card.points()] = []
            count[card.points()].append(card)
        for k in sorted(count, reverse=True):
            if len(count[k]) == 2:
                pairhand = count[k]
                break
        if pairhand:
            for card in hand:
                if card not in pairhand:
                    pairhand.append(card);
                if len(pairhand) > 4:
                    break
        else:
            return False
        return pairhand

if __name__ == "__main__":
    import unittest
    from card import Card
    class TestRules(unittest.TestCase):
        def setUp(self):
            pass
        def test_constants(self):
            self.assertIn('straightflush', Rules.RANKING)
            self.assertIn('A', Rules.POINTS)
        def test_quads(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('10', 'C', 10))
            hand1.append(Card('10', 'S', 10))
            hand1.append(Card('3', 'C', 3))
            hand1.append(Card('10', 'H', 10))
            hand1.append(Card('10', 'D', 10))
            self.assertNotEqual(rules.isquads(hand1), False)
            hand2 = []
            hand2.append(Card('5', 'C', 5))
            hand2.append(Card('10', 'S', 10))
            hand2.append(Card('3', 'C', 3))
            hand2.append(Card('10', 'D', 10))
            hand2.append(Card('10', 'H', 10))
            self.assertEqual(rules.isquads(hand2), False)
        def test_fullhouse(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('10', 'C', 10))
            hand1.append(Card('10', 'S', 10))
            hand1.append(Card('3', 'C', 3))
            hand1.append(Card('10', 'H', 10))
            hand1.append(Card('3', 'D', 3))
            self.assertNotEqual(rules.isfullhouse(hand1), False)
            hand2 = []
            hand2.append(Card('5', 'C', 5))
            hand2.append(Card('10', 'S', 10))
            hand2.append(Card('3', 'C', 3))
            hand2.append(Card('10', 'D', 10))
            hand2.append(Card('10', 'H', 10))
            self.assertEqual(rules.isfullhouse(hand2), False)
        def test_flush(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('10', 'C', 10))
            hand1.append(Card('9', 'C', 9))
            hand1.append(Card('K', 'C', 13))
            hand1.append(Card('5', 'C', 5))
            hand1.append(Card('3', 'C', 3))
            self.assertNotEqual(rules.isflush(hand1), False)
            hand2 = []
            hand2.append(Card('10', 'C', 10))
            hand2.append(Card('9', 'C', 9))
            hand2.append(Card('K', 'C', 13))
            hand2.append(Card('5', 'D', 5))
            hand2.append(Card('3', 'C', 3))
            self.assertEqual(rules.isflush(hand2), False)
        def test_straight(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('Q', 'H', 12))
            hand1.append(Card('J', 'C', 11))
            hand1.append(Card('10', 'S', 10))
            hand1.append(Card('9', 'C', 9))
            hand1.append(Card('8', 'D', 8))
            self.assertNotEqual(rules.isstraight(hand1), False)
            hand2 = []
            hand2.append(Card('10', 'H', 10))
            hand2.append(Card('3', 'C', 3))
            hand2.append(Card('J', 'S', 11))
            hand2.append(Card('8', 'C', 8))
            hand2.append(Card('Q', 'D', 12))
            self.assertEqual(rules.isstraight(hand2), False)
        def test_trips(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('10', 'C', 10))
            hand1.append(Card('10', 'S', 10))
            hand1.append(Card('3', 'C', 3))
            hand1.append(Card('5', 'H', 5))
            hand1.append(Card('10', 'D', 10))
            self.assertNotEqual(rules.istrips(hand1), False)
            hand2 = []
            hand2.append(Card('5', 'C', 5))
            hand2.append(Card('10', 'S', 10))
            hand2.append(Card('3', 'C', 3))
            hand2.append(Card('10', 'D', 10))
            hand2.append(Card('7', 'H', 7))
            self.assertEqual(rules.istrips(hand2), False)
        def test_twopairs(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('10', 'C', 10))
            hand1.append(Card('10', 'S', 10))
            hand1.append(Card('3', 'C', 3))
            hand1.append(Card('5', 'H', 5))
            hand1.append(Card('5', 'D', 5))
            self.assertNotEqual(rules.istwopair(hand1), False)
            hand2 = []
            hand2.append(Card('5', 'C', 5))
            hand2.append(Card('10', 'S', 10))
            hand2.append(Card('3', 'C', 3))
            hand2.append(Card('10', 'D', 10))
            hand2.append(Card('7', 'H', 7))
            self.assertEqual(rules.istwopair(hand2), False)
        def test_pair(self):
            rules = Rules()
            hand1 = []
            hand1.append(Card('10', 'C', 10))
            hand1.append(Card('10', 'S', 10))
            hand1.append(Card('3', 'C', 3))
            hand1.append(Card('5', 'H', 5))
            hand1.append(Card('4', 'D', 4))
            self.assertNotEqual(rules.ispair(hand1), False)
            hand2 = []
            hand2.append(Card('5', 'C', 5))
            hand2.append(Card('10', 'S', 10))
            hand2.append(Card('3', 'C', 3))
            hand2.append(Card('8', 'D', 8))
            hand2.append(Card('7', 'H', 7))
            self.assertEqual(rules.ispair(hand2), False)
    unittest.main()