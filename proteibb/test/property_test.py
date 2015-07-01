import unittest

from proteibb.core import properties

class PropertyTestCase(unittest.TestCase):

    def test_string_property(self):
        slp = properties.StringProperty('sp')
        self.assertEqual(slp.get_name(), 'sp')
        self.assertEqual(slp.is_optional(), False)
        self.assertRaises(SyntaxError, slp.set_value, 12345)
        self.assertRaises(SyntaxError, slp.set_value, '')
        self.assertEqual(slp.set_value("test-string"), None)
        self.assertEqual(slp.get_value(), "test-string")

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
        vp = properties.VersionProperty()
        self.assertEqual(vp.get_name(), 'version')
        self.assertEqual(vp.get_value(), '')
        self.assertEqual(vp.is_optional(), False)
        self.assertRaises(SyntaxError, vp.set_value, 123456)
        self.assertRaises(SyntaxError, vp.set_value, 'abcd')
        self.assertRaises(SyntaxError, vp.set_value, '')
        self.assertRaises(SyntaxError, vp.set_value, '.')
        self.assertRaises(SyntaxError, vp.set_value, '.0.0')
        self.assertRaises(SyntaxError, vp.set_value, '4.')
        self.assertRaises(SyntaxError, vp.set_value, 'a.b.c')
        self.assertRaises(SyntaxError, vp.set_value, '4.0.a')
        self.assertEqual(vp.set_value('1.0.0'), None)
        self.assertEqual(vp.get_value(), [1, 0, 0])
        self.assertEqual(vp.set_value('12'), None)
        self.assertEqual(vp.get_value(), [12])
        self.assertEqual(vp.set_value('5.2'), None)
        self.assertEqual(vp.get_value(), [5, 2])

    def test_dependencies_property(self):
        dp = properties.DependencyProperty()
        self.assertEqual(dp.get_name(), 'dependency')
        self.assertEqual(dp.get_value(), None)
        self.assertEqual(dp.is_optional(), False)
        self.assertRaises(SyntaxError, dp.set_value, 12345)
        self.assertRaises(SyntaxError, dp.set_value, '')
        self.assertRaises(SyntaxError, dp.set_value, ':')
        self.assertRaises(SyntaxError, dp.set_value, ':1.0')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:1..0')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:1.0.0:')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:<1000')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:=1.0.0')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:.0.0')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:4.0:4.')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a: 2.0')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:a')
        self.assertRaises(SyntaxError, dp.set_value, 'lib_a:1.2.5.')
        self.assertEqual(dp.set_value('lib_a'), None)
        self.assertEqual(dp.get_value().get_name(), 'lib_a')
        self.assertEqual(dp.get_value().get_versions(), [])
        self.assertEqual(dp.set_value('lib_b:1.0:2.0'), None)
        self.assertEqual(dp.get_value().get_name(), 'lib_b')
        self.assertEqual(dp.get_value().get_versions(), [[1, 0], [2, 0]])
        self.assertEqual(dp.set_value('lib_c:1.0'), None)
        self.assertEqual(dp.get_value().get_name(), 'lib_c')
        self.assertEqual(dp.get_value().get_versions(), [[1, 0]])
        self.assertEqual(dp.set_value('lib_d:1.0.5:1.0.7:1.1.14'), None)
        self.assertEqual(dp.get_value().get_name(), 'lib_d')
        self.assertEqual(dp.get_value().get_versions(), [[1, 0, 5], [1, 0, 7], [1, 1, 14]])

    def test_sub_property(self):

        class SubPropertyHandler(properties.Property.Handler):

            def __init__(self,  data):
                internal_props = [
                    properties.StringProperty('test-prop-str'),
                    properties.EnumerationProperty('test-prop-enum', ['a', 'b', 'c'], is_optional=True)
                ]
                properties.Property.Handler.__init__(self, internal_props, data)

        sp = properties.SubProperty('extensions', SubPropertyHandler)
        self.assertEqual(sp.get_name(), 'extensions')
        self.assertEqual(sp.get_value(), None)
        self.assertEqual(sp.is_optional(), True)
        self.assertRaises(SyntaxError, sp.set_value, 12345)
        self.assertRaises(SyntaxError, sp.set_value, '')
        self.assertRaises(SyntaxError, sp.set_value, [])
        self.assertRaises(SyntaxError, sp.set_value, {'': ''})
        self.assertRaises(SyntaxError, sp.set_value, {'': []})
        self.assertRaises(SyntaxError, sp.set_value, {'test-prop-str': 12345})
        self.assertRaises(SyntaxError, sp.set_value, {'test-prop-str': 'abcde1', 'test-prop-enum': ''})
        self.assertRaises(SyntaxError, sp.set_value, {'test-prop-str': 'abcde2', 'test-prop-enum': 'e'})
        self.assertRaises(SyntaxError, sp.set_value, {'test-prop-enum': 'a'})
        self.assertEqual(sp.set_value({'test-prop-str': 'test-prop-str-value'}), None)
        self.assertEqual(sp.get_value()._properties['test-prop-str'].get_value(), 'test-prop-str-value')
        self.assertEqual(sp.get_value()._properties['test-prop-enum'].get_value(), '')
        self.assertEqual(sp.set_value({'test-prop-str': 'test-prop-str-value-two', 'test-prop-enum': 'b'}), None)
        self.assertEqual(sp.get_value()._properties['test-prop-str'].get_value(), 'test-prop-str-value-two')
        self.assertEqual(sp.get_value()._properties['test-prop-enum'].get_value(), 'b')

    def test_string_list_property(self):
        vlp = properties.PropertyListAdapter('string-list', True, properties.StringProperty)
        self.assertEqual(vlp.get_name(), 'string-list')
        self.assertEqual(vlp.get_value(), [])
        self.assertEqual(vlp.is_optional(), True)
        self.assertRaises(SyntaxError, vlp.set_value, 12345)
        self.assertRaises(SyntaxError, vlp.set_value, '')
        self.assertRaises(SyntaxError, vlp.set_value, [])
        self.assertRaises(SyntaxError, vlp.set_value, [''])
        self.assertRaises(SyntaxError, vlp.set_value, ['abcdef', ''])
        self.assertRaises(SyntaxError, vlp.set_value, ['abcdef', 12345])
        self.assertEqual(vlp.set_value(['abc', 'bcd', 'cde']), None)
        self.assertEqual(vlp.get_value(), ['abc', 'bcd', 'cde'])

    def test_extension_property(self):
        ep = properties.ExtensionAdapter('ext-ada', True, properties.StringProperty)
        self.assertEqual(ep.get_name(), 'ext-ada')
        self.assertEqual(ep.get_value(), None)
        self.assertEqual(ep.is_optional(), True)
        self.assertRaises(SyntaxError, ep.set_value, 12345)
        self.assertRaises(SyntaxError, ep.set_value, "")
        self.assertRaises(SyntaxError, ep.set_value, "+")
        self.assertRaises(SyntaxError, ep.set_value, "-")
        self.assertRaises(SyntaxError, ep.set_value, "++abc")
        self.assertRaises(SyntaxError, ep.set_value, "abc-cde")
        self.assertRaises(SyntaxError, ep.set_value, "abcdefg")
        self.assertEqual(ep.set_value("-test-str"), None)
        self.assertEqual(ep.get_value(), {'ext': '-', 'val': 'test-str'})
        self.assertEqual(ep.set_value("+test-str-other"), None)
        self.assertEqual(ep.get_value(), {'ext': '+', 'val': 'test-str-other'})

    def test_extension_list_property(self):
        pass

if __name__ == '__main__':
    unittest.main()
