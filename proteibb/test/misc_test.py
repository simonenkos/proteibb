import unittest

from proteibb.util import *


class MiscellaneousTestCase(unittest.TestCase):

    def test_version_split(self):
        self.assertRaises(ValueError, split_version, '')
        self.assertRaises(ValueError, split_version, '1.2.')
        self.assertEqual(split_version('1'), [1])
        self.assertEqual(split_version('1.2.3'), [1, 2, 3])

    def test_make_version(self):
        self.assertEqual(make_version([]), '')
        self.assertEqual(make_version([1]), '1')
        self.assertEqual(make_version([1, 2]), '1_2')
        self.assertEqual(make_version([1, 0, 40, 1]), '1_0_40_1')

if __name__ == '__main__':
    unittest.main()
