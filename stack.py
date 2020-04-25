class Stack:
# players chip stack

    def __init__(self, val):
        self.__value = val

    def add(self, val):
        self.__value = self.__value + val

    def subtract(self, val):
        if val > self.__value:
            self.__value = 0
            return
        self.__value = self.__value - val

    def getvalue(self):
        return self.__value

if __name__ == "__main__":
    import unittest
    class TestStack(unittest.TestCase):
        def setUp(self):
            pass
        def test_add(self):
            stack = Stack(5000)
            stack.add(800)
            self.assertEqual(stack.getvalue(), 5800)
        def test_subtract1(self):
            stack = Stack(5000)
            stack.subtract(200)
            self.assertEqual(stack.getvalue(), 4800)
        def test_subtract2(self):
            stack = Stack(500)
            stack.subtract(1000)
            self.assertEqual(stack.getvalue(), 0)
    unittest.main()