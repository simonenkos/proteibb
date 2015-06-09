import unittest

from proteibb.core import source

class PropertyTestCase(unittest.TestCase):

    def test_string_property(self):
        sp = source.StringProperty('name')
        self.assertEqual(sp.get_name(), 'name')
        self.assertRaises(SyntaxError, sp.set_value, 12345)
        self.assertEqual(sp.set_value('string'), None)
        self.assertEqual(sp.get_value(), 'string')

    def test_url_property(self):
        up = source.UrlProperty()
        self.assertEqual(up.get_name(), 'url')
        self.assertEqual(up.is_optional(), False)
        self.assertRaises(SyntaxError, up.set_value, 12345)
        self.assertRaises(SyntaxError, up.set_value, '')
        self.assertRaises(SyntaxError, up.set_value, 'abcdef')
        self.assertRaises(SyntaxError, up.set_value, '://')
        self.assertRaises(SyntaxError, up.set_value, 'github.com/user/project')
        self.assertRaises(SyntaxError, up.set_value, 'http://hg.company\project\path')
        self.assertEqual(up.set_value('http://svn.server.com/db'), None)
        self.assertEqual(up.get_value(), 'http://svn.server.com/db')

    def test_vcs_property(self):
        vp = source.VcsProperty()
        self.assertEqual(vp.get_name(), 'vcs')
        self.assertEqual(vp.is_optional(), False)
        self.assertRaises(SyntaxError, vp.set_value, 12345)
        self.assertRaises(SyntaxError, vp.set_value, '')
        self.assertRaises(SyntaxError, vp.set_value, 'svvn')
        self.assertRaises(SyntaxError, vp.set_value, 'mercurial')
        self.assertEqual(vp.set_value('svn'), None)
        self.assertEqual(vp.get_value(), 'svn')
        self.assertEqual(vp.set_value('git'), None)
        self.assertEqual(vp.get_value(), 'git')
        self.assertEqual(vp.set_value('hg'), None)
        self.assertEqual(vp.get_value(), 'hg')

    def test_version_property(self):
        vp = source.VersionProperty()
        self.assertEqual(vp.get_name(), 'version')
        self.assertEqual(vp.is_optional(), True)
        self.assertRaises(SyntaxError, vp.set_value, 123456)
        self.assertRaises(SyntaxError, vp.set_value, '.')
        self.assertRaises(SyntaxError, vp.set_value, '.0.0')
        self.assertRaises(SyntaxError, vp.set_value, '4.')
        self.assertRaises(SyntaxError, vp.set_value, 'a.b.c')
        self.assertRaises(SyntaxError, vp.set_value, '4.0.a')
        self.assertEqual(vp.set_value('1.0.0'), None)
        self.assertEqual(vp.get_value(), [1, 0, 0])
        self.assertEqual(vp.set_value('12'), None)
        self.assertEqual(vp.get_value(), [12])
        self.assertEqual(vp.set_value('4.0'), None)
        self.assertEqual(vp.get_value(), [4, 0])
        self.assertEqual(vp.set_value(''), None)
        self.assertEqual(vp.get_value(), [])

    def test_dependencies_property(self):
        dp = source.DependenciesProperty()
        self.assertEqual(dp.get_name(), 'dependencies')
        self.assertEqual(dp.is_optional(), True)
        self.assertRaises(SyntaxError, dp.set_value, 12345)
        self.assertRaises(SyntaxError, dp.set_value, '')
        self.assertRaises(SyntaxError, dp.set_value, [''])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a', ''])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a', 'lib_d:'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:1..0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:1.0.0:'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a', 'lib_d', 'lib_c:<<1000'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:=1.0.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:>.0.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:4.0:4.'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:<>2.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:>1.0:>0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a>1.0.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a3.1'])
        # self.assertEqual(dp.set_value(['lib_a:1.0']), None)
        # self.assertEqual(dp.get_value(), ['lib_a:1.0', 'lib_b', 'lib_d:>1.0.0'])


if __name__ == '__main__':
    unittest.main()
