import unittest
from HTMLReport import logger

log = logger()

class Demo1(unittest.TestCase):

    def test_print(self):
        log.info('*'*100)

    def test_hello(self):
        log.info('hello'*10)


if __name__ == '__main__':
    unittest.main()