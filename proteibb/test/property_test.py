import unittest

from proteibb.core.project import properties
from proteibb.util.property_handler import *
from proteibb.util.property import *

class PropertyTestCase(unittest.TestCase):

    def test_string_list_property(self):
        slp = StringsListProperty('slp')
        self.assertEqual(slp.get_name(), 'slp')
        self.assertEqual(slp.is_optional(), False)
        self.assertRaises(SyntaxError, slp.set_value, 12345)
        self.assertRaises(SyntaxError, slp.set_value, '')
        self.assertRaises(SyntaxError, slp.set_value, [""])
        self.assertRaises(SyntaxError, slp.set_value, ['x86', ''])
        self.assertRaises(SyntaxError, slp.set_value, ['arm', 12345])
        self.assertEqual(slp.set_value(['x86', 'arm']), None)
        self.assertEqual(slp.get_value(), ['x86', 'arm'])

    def test_type_property(self):
        tp = properties.TypeProperty()
        self.assertEqual(tp.get_name(), 'type')
        self.assertEqual(tp.get_value(), "")
        self.assertEqual(tp.is_optional(), False)
        self.assertRaises(SyntaxError, tp.set_value, 12345)
        self.assertRaises(SyntaxError, tp.set_value, '')
        self.assertRaises(SyntaxError, tp.set_value, 'abc')
        self.assertRaises(SyntaxError, tp.set_value, 'application ')
        self.assertEqual(tp.set_value('library'), None)
        self.assertEqual(tp.get_value(), 'library')

    def test_url_property(self):
        up = properties.UrlProperty()
        self.assertEqual(up.get_name(), 'url')
        self.assertEqual(up.get_value(), "")
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
        vp = properties.VcsProperty()
        self.assertEqual(vp.get_name(), 'vcs')
        self.assertEqual(vp.get_value(), "")
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
        vp = properties.VersionsProperty()
        self.assertEqual(vp.get_name(), 'versions')
        self.assertEqual(vp.get_value(), [])
        self.assertEqual(vp.is_optional(), True)
        self.assertRaises(SyntaxError, vp.set_value, 123456)
        self.assertRaises(SyntaxError, vp.set_value, 'abcd')
        self.assertRaises(SyntaxError, vp.set_value, [''])
        self.assertRaises(SyntaxError, vp.set_value, ['.'])
        self.assertRaises(SyntaxError, vp.set_value, ['.0.0'])
        self.assertRaises(SyntaxError, vp.set_value, ['4.'])
        self.assertRaises(SyntaxError, vp.set_value, ['a.b.c'])
        self.assertRaises(SyntaxError, vp.set_value, ['4.0.a'])
        self.assertRaises(SyntaxError, vp.set_value, ['1.2.3', '1.'])
        self.assertEqual(vp.set_value(['1.0.0']), None)
        self.assertEqual(vp.get_value(), [[1, 0, 0]])
        self.assertEqual(vp.set_value(['12']), None)
        self.assertEqual(vp.get_value(), [[12]])
        self.assertEqual(vp.set_value(['4.0', '5.2']), None)
        self.assertEqual(vp.get_value(), [[4, 0], [5, 2]])

    def test_dependencies_property(self):
        dp = properties.DependenciesProperty()
        self.assertEqual(dp.get_name(), 'dependencies')
        self.assertEqual(dp.get_value(), [])
        self.assertEqual(dp.is_optional(), True)
        self.assertRaises(SyntaxError, dp.set_value, 12345)
        self.assertRaises(SyntaxError, dp.set_value, '')
        self.assertRaises(SyntaxError, dp.set_value, [''])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a', ''])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a', 'lib_d:'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:1..0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:1.0.0:'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a', 'lib_d', 'lib_c:<<1000'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:>=1.0.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:>.0.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:4.0:4.'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:<>2.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:>1.0:>a'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a>1.0.0'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a3.1'])
        self.assertRaises(SyntaxError, dp.set_value, ['lib_a:>1.5.0:<1.2.5'])
        self.assertEqual(dp.set_value(['lib_a']), None)
        self.assertEqual(dp.get_value()[0].get_name(), 'lib_a')
        self.assertEqual(dp.get_value()[0].get_versions(), {'ver': [], 'min': None, 'max': None})
        self.assertEqual(dp.set_value(['lib_a:=1.0:=2.0']), None)
        self.assertEqual(dp.get_value()[0].get_name(), 'lib_a')
        self.assertEqual(dp.get_value()[0].get_versions(), {'ver': [[1, 0], [2, 0]], 'min': None, 'max': None})
        self.assertEqual(dp.set_value(['lib_b:>1.0:<2.0']), None)
        self.assertEqual(dp.get_value()[0].get_name(), 'lib_b')
        self.assertEqual(dp.get_value()[0].get_versions(), {'ver': [], 'min': [1, 0], 'max': [2, 0]})
        self.assertEqual(dp.set_value(['lib_c:=1.0:>2.0']), None)
        self.assertEqual(dp.get_value()[0].get_name(), 'lib_c')
        self.assertEqual(dp.get_value()[0].get_versions(), {'ver': [], 'min': [2, 0], 'max': None})
        self.assertEqual(dp.set_value(['lib_d:=2.0:>2.0']), None)
        self.assertEqual(dp.get_value()[0].get_name(), 'lib_d')
        self.assertEqual(dp.get_value()[0].get_versions(), {'ver': [[2, 0]], 'min': [2, 0], 'max': None})

    def test_extensions_property(self):

        class TestPropertyHandler(PropertyHandler):

            def __init__(self,  data):
                internal_props = [
                    StringProperty('test-prop-str'),
                    EnumerationProperty('test-prop-enum', ['a', 'b', 'c'], is_optional=True)
                ]
                PropertyHandler.__init__(self, internal_props, data)

        ep = properties.ExtensionsProperty('extensions', TestPropertyHandler)
        self.assertEqual(ep.get_name(), 'extensions')
        self.assertEqual(ep.get_value(), {})
        self.assertEqual(ep.is_optional(), True)
        self.assertRaises(SyntaxError, ep.set_value, 12345)
        self.assertRaises(SyntaxError, ep.set_value, '')
        self.assertRaises(SyntaxError, ep.set_value, [])
        self.assertRaises(SyntaxError, ep.set_value, {'': ''})
        self.assertRaises(SyntaxError, ep.set_value, {'': []})
        self.assertRaises(SyntaxError, ep.set_value, {'test-prop-str': 12345})
        self.assertRaises(SyntaxError, ep.set_value, {'test-prop-str': 'abcde1', 'test-prop-enum': ''})
        self.assertRaises(SyntaxError, ep.set_value, {'test-prop-str': 'abcde2', 'test-prop-enum': 'e'})
        self.assertRaises(SyntaxError, ep.set_value, {'test-prop-enum': 'a'})
        self.assertEqual(ep.set_value({'test-prop-str': 'test-prop-str-value'}), None)
        self.assertEqual(ep.get_value()._properties['test-prop-str'].get_value(), 'test-prop-str-value')
        self.assertEqual(ep.get_value()._properties['test-prop-enum'].get_value(), '')
        self.assertEqual(ep.set_value({'test-prop-str': 'test-prop-str-value-two', 'test-prop-enum': 'b'}), None)
        self.assertEqual(ep.get_value()._properties['test-prop-str'].get_value(), 'test-prop-str-value-two')
        self.assertEqual(ep.get_value()._properties['test-prop-enum'].get_value(), 'b')

if __name__ == '__main__':
    unittest.main()
