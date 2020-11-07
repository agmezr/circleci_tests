import unittest
import time


class MyTestCase(unittest.TestCase):

    def test_something(self):
        time.sleep(15)
        self.assertTrue(True)

    def test_some_1(self):
        time.sleep(5)
        self.assertTrue(True)

    def test_some_2(self):
        time.sleep(5)
        self.assertTrue(True)

    def test_some_3(self):
        time.sleep(5)
        self.assertTrue(True)

    def test_some_4(self):
        time.sleep(5)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
