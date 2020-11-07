import unittest
import time

class ATests(unittest.TestCase):

    def test_a(self):
        time.sleep(3)
        self.assertTrue(True)

    def test_b(self):
        time.sleep(10)
        self.assertTrue(True)

    def test_c(self):
        time.sleep(30)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
