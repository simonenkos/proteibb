import unittest

from proteibb.util.filter import *

class FilterTestCase(unittest.TestCase):

    def test_empty_filter(self):
        self.assertRaises(TypeError, Filter, None)

    def test_open_filter(self):
        f = Filter(lambda x: True)
        self.assertEqual(f([1, 2, 'a', None, 'b']), [1, 2, 'a', None, 'b'])

    def test_altering_filter(self):
        f = Filter((lambda x: x <= 10), (lambda lst: [str(y - 5) for y in lst]))
        self.assertEqual(f(range(5, 15)), ['0', '1', '2', '3', '4', '5'])

    def test_filter_set_serial_processing(self):
        f1 = Filter(lambda x: x > 20)
        f2 = Filter(lambda x: x < 30)
        f3 = Filter(lambda x: x % 2 == 0)
        fsp = apply_filter_set_serial(f1)
        self.assertEqual(fsp(range(18, 32, 1)), [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
        fsp = apply_filter_set_serial(f1, f2)
        self.assertEqual(fsp(range(18, 32, 1)), [21, 22, 23, 24, 25, 26, 27, 28, 29])
        fsp = apply_filter_set_serial(f1, f2, f3)
        self.assertEqual(fsp(range(18, 32, 1)), [22, 24, 26, 28])

    def test_filter_set_parallel_processing(self):
        f1 = Filter(lambda x: x > 5)
        f2 = Filter(lambda x: x % 2 != 0)
        f3 = Filter(lambda x: x % 3 != 0)
        fsp = apply_filter_set_parallel(f1)
        self.assertEqual(fsp(range(5, 12, 1)), [6, 7, 8, 9, 10, 11])
        fsp = apply_filter_set_parallel(f1, f2)
        self.assertEqual(fsp(range(5, 12, 1)), [6, 7, 8, 9, 10, 11, 5, 7, 9, 11])
        fsp = apply_filter_set_parallel(f1, f2, f3)
        self.assertEqual(fsp(range(5, 12, 1)), [6, 7, 8, 9, 10, 11, 5, 7, 9, 11, 5, 7, 8, 10, 11])

if __name__ == '__main__':
    unittest.main()
