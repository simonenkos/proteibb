import unittest

from proteibb.util.filter import *

class FilterTestCase(unittest.TestCase):

    def test_empty_filter(self):
        self.assertRaises(TypeError, Filter, None)

    def test_open_filter(self):
        f = Filter(lambda x: True)
        self.assertEqual(f([1, 2, 'a', None, 'b']), [1, 2, 'a', None, 'b'])

    def test_filter_set_processing(self):
        f1 = Filter(lambda x: x > 20)
        f2 = Filter(lambda x: x < 30)
        f3 = Filter(lambda x: x % 2 == 0)
        fsp = apply_filter_set(f1)
        self.assertEqual(fsp(range(18, 32, 1)), [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
        fsp = apply_filter_set(f1, f2)
        self.assertEqual(fsp(range(18, 32, 1)), [21, 22, 23, 24, 25, 26, 27, 28, 29])
        fsp = apply_filter_set(f1, f2, f3)
        self.assertEqual(fsp(range(18, 32, 1)), [22, 24, 26, 28])

if __name__ == '__main__':
    unittest.main()
