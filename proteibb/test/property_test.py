import unittest

from proteibb.core import properties
from proteibb.util.factory import ObjectFactory


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

    def test_sub_property(self):

        class SubPropertyHandler(properties.Property.Handler):

            def __init__(self,  data):
                internal_props = [
                    properties.StringProperty('test-prop-str'),
                    properties.EnumerationProperty('test-prop-enum', ['a', 'b', 'c'], is_optional=True)
                ]
                properties.Property.Handler.__init__(self, internal_props, data)

        sp = properties.SubProperty('extensions', True, SubPropertyHandler)
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
        self.assertEqual(ep.get_value(), properties.Extension('-', 'test-str'))
        self.assertEqual(ep.set_value("+test-str-other"), None)
        self.assertEqual(ep.get_value(), properties.Extension('+', 'test-str-other'))

    def test_extension_list_property(self):
        elp = properties.PropertyListAdapter('elp', False, properties.ExtensionAdapter,
                                             properties.PropertyAdapter.Arguments(True, properties.StringProperty))
        self.assertEqual(elp.get_name(), 'elp')
        self.assertEqual(elp.get_value(), [])
        self.assertEqual(elp.is_optional(), False)
        self.assertRaises(SyntaxError, elp.set_value, 12345)
        self.assertRaises(SyntaxError, elp.set_value, '')
        self.assertRaises(SyntaxError, elp.set_value, [])
        self.assertRaises(SyntaxError, elp.set_value, [12345, 54321])
        self.assertRaises(SyntaxError, elp.set_value, [''])
        self.assertRaises(SyntaxError, elp.set_value, ['abc', 'cde'])
        self.assertEqual(elp.set_value(['-aaa', '+bbb']), None)
        self.assertEqual(len(elp.get_value()), 2)
        self.assertEqual(elp.get_value()[0], properties.Extension('-', 'aaa'))
        self.assertEqual(elp.get_value()[1], properties.Extension('+', 'bbb'))

    def test_options_factory_property(self):

        class TestGroup:

            def __init__(self, fhc_data, factory):
                self._data = fhc_data
                self._factory = factory

            def get_data(self):
                return self._data

            def get_factory(self):
                return self._factory

        data = {
            'x': 1,
            'y': 2,
            'z': 3,
        }
        of = ObjectFactory()
        fp = properties.GroupProperty('fp', True, of, TestGroup)
        self.assertEqual(fp.get_name(), 'fp')
        self.assertEqual(fp.get_value(), {})
        self.assertEqual(fp.is_optional(), True)
        self.assertRaises(SyntaxError, fp.set_value, 12345)
        self.assertRaises(SyntaxError, fp.set_value, '')
        self.assertRaises(SyntaxError, fp.set_value, [])
        self.assertEqual(fp.set_value(data), None)
        self.assertEqual(fp.get_value().get_data(), data)
        self.assertEqual(fp.get_value().get_factory(), of)

    def test_path_property(self):
        pp = properties.PathProperty('pp', True)
        self.assertEqual(pp.get_name(), 'pp')
        self.assertEqual(pp.get_value(), '')
        self.assertEqual(pp.is_optional(), True)
        self.assertRaises(SyntaxError, pp.set_value, 12345)
        self.assertRaises(SyntaxError, pp.set_value, '')
        self.assertRaises(SyntaxError, pp.set_value, [])
        self.assertRaises(SyntaxError, pp.set_value, '//p/')
        self.assertRaises(SyntaxError, pp.set_value, 'path/to/file')
        self.assertEqual(pp.set_value('/bin'), None)
        self.assertEqual(pp.get_value(), '/bin')

if __name__ == '__main__':
    unittest.main()
