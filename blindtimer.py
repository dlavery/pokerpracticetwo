import time

class BlindTimer:

    __BLINDS = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 3000, 4000, 5000, 10000, 20000, 40000, 50000]

    def __init__(self, blindinterval):
        self.__blindinterval = blindinterval
        self.__blinds = (self.__BLINDS[0], self.__BLINDS[0] * 2)
        self.__blindlimit = len(self.__BLINDS) - 1
        self.__blindcount = 0
        self.__starttime = time.time()

    def getblinds(self):
        ts = time.time()
        blindsup = (ts - self.__starttime) >= self.__blindinterval
        if blindsup:
            if self.__blindcount < self.__blindlimit:
                self.__blindcount = self.__blindcount + 1
            self.__blinds = (self.__BLINDS[self.__blindcount], self.__BLINDS[self.__blindcount] * 2)
            self.__starttime = ts
        self.__pot = 0
        self.__actcount = 0
        self.__round = ''
        self.__betindex = 0
        self.__playercount = 0
        return self.__blinds

    def gettimeremaining(self):
        return (self.__starttime + self.__blindinterval - time.time())

if __name__ == "__main__":
    import time
    import unittest
    class TestBlindTimer(unittest.TestCase):
        def setUp(self):
            pass

        def test_blinds(self):
            b = BlindTimer(1)
            blinds = b.getblinds()
            self.assertEqual(blinds, (100, 200))
            time.sleep(1)
            blinds = b.getblinds()
            self.assertEqual(blinds, (200, 400))
            time.sleep(1)
            blinds = b.getblinds()
            self.assertEqual(blinds, (300, 600))
            time.sleep(3)
            blinds = b.getblinds()
            self.assertEqual(blinds, (400, 800))

        def test_timer(self):
            b = BlindTimer(60)
            time.sleep(2)
            remaining = b.gettimeremaining()
            self.assertGreater(remaining, 50)
            self.assertLess(remaining, 58)

    unittest.main()
