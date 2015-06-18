import unittest

from proteibb.core.source import source as src
from proteibb.core.source import source_factory

from proteibb.core.source.details.automation import Automation
from proteibb.core.source.details.production import Production
from proteibb.core.source.details.user import User

class SourceTestCase(unittest.TestCase):

    def test_source_properties_setup_all(self):
        data = {
            'name': 'lib_source',
            'vcs': 'git',
            'url': 'http://github.com/user/project'
        }
        details = {
            'branch': 'master',
            'versions': ['1.0.0.24', '1.0.0.26'],
            'revision': 'head',
            'dependencies': ['lib:=1.0']
        }
        s = src.Source(data, details)
        self.assertEqual(s.name().get_value(), 'lib_source')
        self.assertEqual(s.vcs().get_value(), 'git')
        self.assertEqual(s.url().get_value(), 'http://github.com/user/project')
        self.assertEqual(s.branch().get_value(), 'master')
        self.assertEqual(s.versions().get_value(), [[1, 0, 0, 24], [1, 0, 0, 26]])
        self.assertEqual(s.revision().get_value(), 'head')
        self.assertEqual(s.dependencies().get_value()[0].get_name(), 'lib')
        self.assertEqual(s.dependencies().get_value()[0].get_versions(),
                         {'ver': [[1, 0]], 'min': None, 'max': None})

    def test_source_properties_setup_optional(self):
        data = {
            'name': 'lib',
            'vcs': 'hg',
            'url': 'http://mercurial'
        }
        details = {
            'revision': '123:456789',
        }
        s = src.Source(data, details)
        self.assertEqual(s.name().get_value(), 'lib')
        self.assertEqual(s.vcs().get_value(), 'hg')
        self.assertEqual(s.url().get_value(), 'http://mercurial')
        self.assertEqual(s.branch().get_value(), '')
        self.assertEqual(s.versions().get_value(), [])
        self.assertEqual(s.revision().get_value(), '123:456789')
        self.assertEqual(s.dependencies().get_value(), [])

    def test_source_factory_no_details(self):
        data = {
            'name': 'lib_source',
            'vcs': 'svn',
            'url': 'http://subversion',
        }
        self.assertRaises(SyntaxError, source_factory.make, data)

    def test_source_factory_empty_details(self):
        data = {
            'name': 'lib_source',
            'vcs': 'svn',
            'url': 'http://subversion',
            'automation': [],
            'production': [],
            'user': [],
        }
        sources = source_factory.make(data)
        self.assertEqual(sources, [])

    def test_source_factory_automation_only(self):
        data = {
            'name': 'libx',
            'vcs': 'svn',
            'url': 'http://subversion',
            'automation': [
                {
                    'branch': 'trunk',
                    'revision': 'HEAD'
                },
                {
                    'branch': 'branches/release_1_0',
                    'revision': 'HEAD',
                    'dependencies': ['liby:=1.5', 'libz:>3.0']
                }
            ],
            'production': [],
            'user': [],
        }
        sources = source_factory.make(data)
        self.assertEqual(len(sources), 2)
        self.assertEqual(sources[0].name().get_value(), 'libx')
        self.assertEqual(sources[0].vcs().get_value(), 'svn')
        self.assertEqual(sources[0].url().get_value(), 'http://subversion')
        self.assertEqual(sources[0].branch().get_value(), 'trunk')
        self.assertEqual(sources[0].versions().get_value(), [])
        self.assertEqual(sources[0].revision().get_value(), 'HEAD')
        self.assertEqual(sources[0].dependencies().get_value(), [])
        self.assertEqual(sources[1].name().get_value(), 'libx')
        self.assertEqual(sources[1].vcs().get_value(), 'svn')
        self.assertEqual(sources[1].url().get_value(), 'http://subversion')
        self.assertEqual(sources[1].branch().get_value(), 'branches/release_1_0')
        self.assertEqual(sources[1].versions().get_value(), [])
        self.assertEqual(sources[1].revision().get_value(), 'HEAD')
        self.assertEqual(len(sources[1].dependencies().get_value()), 2)
        self.assertEqual(sources[1].dependencies().get_value()[0].get_name(), 'liby')
        self.assertEqual(sources[1].dependencies().get_value()[0].get_versions(),
                         {'ver': [[1, 5]], 'min': None, 'max': None})
        self.assertEqual(sources[1].dependencies().get_value()[1].get_name(), 'libz')
        self.assertEqual(sources[1].dependencies().get_value()[1].get_versions(),
                         {'ver': [], 'min': [3, 0], 'max': None})

    def test_source_factory_production_only(self):
        data = {
            'name': 'libx',
            'vcs': 'svn',
            'url': 'http://subversion',
            'automation': [],
            'production': [
                {
                    'branch': 'branches/R10',
                    'versions': ['1.0', '1.1', '1.2', '1.3'],
                    'revision': 'HEAD'
                },
                {
                    'branch': 'branches/R15',
                    'versions': ['1.5'],
                    'revision': 'HEAD'
                },
                {
                    'branch': 'branches/R23',
                    'versions': ['2.3'],
                    'revision': 'HEAD',
                    'dependencies': ['libz:=1.7:=1.8:=1.9']
                }
            ],
            'user': []
        }
        sources = source_factory.make(data)
        self.assertEqual(len(sources), 3)
        self.assertEqual(sources[0].name().get_value(), 'libx')
        self.assertEqual(sources[0].vcs().get_value(), 'svn')
        self.assertEqual(sources[0].url().get_value(), 'http://subversion')
        self.assertEqual(sources[0].branch().get_value(), 'branches/R10')
        self.assertEqual(sources[0].versions().get_value(), [[1, 0], [1, 1], [1, 2], [1, 3]])
        self.assertEqual(sources[0].revision().get_value(), 'HEAD')
        self.assertEqual(sources[0].dependencies().get_value(), [])
        self.assertEqual(sources[1].name().get_value(), 'libx')
        self.assertEqual(sources[1].vcs().get_value(), 'svn')
        self.assertEqual(sources[1].url().get_value(), 'http://subversion')
        self.assertEqual(sources[1].branch().get_value(), 'branches/R15')
        self.assertEqual(sources[1].versions().get_value(), [[1, 5]])
        self.assertEqual(sources[1].revision().get_value(), 'HEAD')
        self.assertEqual(sources[1].dependencies().get_value(), [])
        self.assertEqual(sources[2].name().get_value(), 'libx')
        self.assertEqual(sources[2].vcs().get_value(), 'svn')
        self.assertEqual(sources[2].url().get_value(), 'http://subversion')
        self.assertEqual(sources[2].branch().get_value(), 'branches/R23')
        self.assertEqual(sources[2].versions().get_value(), [[2, 3]])
        self.assertEqual(sources[2].revision().get_value(), 'HEAD')
        self.assertEqual(len(sources[2].dependencies().get_value()), 1)
        self.assertEqual(sources[2].dependencies().get_value()[0].get_name(), 'libz')
        self.assertEqual(sources[2].dependencies().get_value()[0].get_versions(),
                         {'ver': [[1, 7], [1, 8], [1, 9]], 'min': None, 'max': None})

    def test_source_factory_user_only(self):
        data = {
            'name': 'liba',
            'vcs': 'hg',
            'url': 'http://mercurial',
            'automation': [],
            'production': [],
            'user': [
                {
                    'branch': 'default',
                    'versions': ['1.23.5.60'],
                    'specification': 'liba-bug-x'
                }
            ]
        }
        sources = source_factory.make(data)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].name().get_value(), 'liba')
        self.assertEqual(sources[0].vcs().get_value(), 'hg')
        self.assertEqual(sources[0].url().get_value(), 'http://mercurial')
        self.assertEqual(sources[0].branch().get_value(), 'default')
        self.assertEqual(sources[0].versions().get_value(), [[1, 23, 5, 60]])
        self.assertEqual(sources[0].revision().get_value(), '')
        self.assertEqual(sources[0].dependencies().get_value(), [])
        self.assertEqual(sources[0].specification().get_value(), 'liba-bug-x')

if __name__ == '__main__':
    unittest.main()
