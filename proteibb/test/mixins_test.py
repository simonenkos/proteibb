import unittest

from proteibb.util.extensible_mixin import ExtensibleMixin


class ExtensibleMixinTestCase(unittest.TestCase):

    class EM1(ExtensibleMixin):

        def __init__(self, data):
            self._container = data
            ExtensibleMixin.__init__(self, self._container)

        def get(self):
            return self._container

    class EM2(EM1):

        def __init__(self, data):
            ExtensibleMixinTestCase.EM1.__init__(self, data)

        def include(self, value):
            self._container = value

    def test_extensible_mixin_object_container(self):
        data = 'abcdef'
        emt = ExtensibleMixinTestCase.EM1(data)
        self.assertEqual(emt.get(), 'abcdef')
        self.assertEqual(emt.include('a'), None)
        self.assertEqual(emt.get(), 'abcdef')
        self.assertEqual(emt.exclude('b'), True)
        self.assertEqual(emt.get(), 'abcdef')

    def test_extensible_mixin_object_with_mixin_container(self):
        data = ExtensibleMixinTestCase.EM2('abcdef')
        emt = ExtensibleMixinTestCase.EM1(data)
        self.assertTrue(isinstance(emt.get(), ExtensibleMixin))
        self.assertEqual(emt.get().get(), 'abcdef')
        self.assertEqual(emt.include('fedcba'), None)
        self.assertEqual(emt.get().get(), 'fedcba')
        self.assertEqual(emt.include(123456789), None)
        self.assertEqual(emt.get().get(), 123456789)
        self.assertEqual(emt.exclude(123456789), True)
        self.assertEqual(emt.get().get(), 123456789)

    def test_extensible_mixin_list_container(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        emt = ExtensibleMixinTestCase.EM1(data)
        self.assertEqual(emt.get(), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(emt.include(0), None)
        self.assertEqual(emt.get(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        self.assertEqual(emt.exclude(5), False)
        self.assertEqual(emt.get(), [1, 2, 3, 4, 6, 7, 8, 9, 0])
        self.assertEqual(emt.exclude(1), False)
        self.assertEqual(emt.get(), [2, 3, 4, 6, 7, 8, 9, 0])
        self.assertEqual(emt.exclude(2), False)
        self.assertEqual(emt.get(), [3, 4, 6, 7, 8, 9, 0])
        self.assertEqual(emt.exclude(3), False)
        self.assertEqual(emt.get(), [4, 6, 7, 8, 9, 0])
        self.assertEqual(emt.exclude(4), False)
        self.assertEqual(emt.get(), [6, 7, 8, 9, 0])
        self.assertEqual(emt.exclude(6), False)
        self.assertEqual(emt.get(), [7, 8, 9, 0])
        self.assertEqual(emt.exclude(7), False)
        self.assertEqual(emt.get(), [8, 9, 0])
        self.assertEqual(emt.exclude(8), False)
        self.assertEqual(emt.get(), [9, 0])
        self.assertEqual(emt.exclude(9), False)
        self.assertEqual(emt.get(), [0])
        self.assertEqual(emt.exclude(0), True)
        self.assertEqual(emt.get(), [])
        self.assertEqual(emt.include(11), None)
        self.assertEqual(emt.get(), [11])
        self.assertEqual(emt.include(15), None)
        self.assertEqual(emt.get(), [11, 15])
        self.assertEqual(emt.include(13), None)
        self.assertEqual(emt.get(), [11, 15, 13])
        self.assertEqual(emt.include(15), None)
        self.assertEqual(emt.get(), [11, 15, 13])
        self.assertEqual(emt.exclude(17), False)
        self.assertEqual(emt.get(), [11, 15, 13])
        self.assertEqual(emt.include('abc'), None)
        self.assertEqual(emt.get(), [11, 15, 13, 'abc'])

    def test_extensible_mixin_list_mixins_container(self):
        data = [ExtensibleMixinTestCase.EM2('first'), ExtensibleMixinTestCase.EM2('second')]
        emt = ExtensibleMixinTestCase.EM1(data)


if __name__ == '__main__':
    unittest.main()
