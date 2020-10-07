import unittest

class Demo1(unittest.TestCase):

    def test_add(self):
        print(1+2)

    def test_divide(self):
        print(4*2)


if __name__ == '__main__':
    unittest.main()
