import unittest
from HTMLReport import logger


class Demo1(unittest.TestCase):
    "TEST测试"

    @classmethod
    def setUpClass(cls):
        print('aaa')


    @classmethod
    def tearDownClass(cls):
        print('bbbb')

    def test_print(self):
        "测试测试测试测试"
        logger().info('*'*100)
        logger().info('*' * 100)
        self.fail()

    def test_hello(self):
        "这个已经搞定了，哈哈哈哈哈哈"
        logger().error('hello'*10)
        logger().error('hello'*10)
        logger().info()


if __name__ == '__main__':
    unittest.main()