import unittest

from proteibb.core.project import project
from proteibb.core.project import detail

class ProjectTestCase(unittest.TestCase):

    def test_project_no_details(self):
        data = {
            'name': 'project',
            'type': 'application',
            'vcs': 'svn',
            'url': 'http://subversion',
            'platforms': ['platformx', 'platformy'],
        }
        self.assertRaises(SyntaxError, project.Project, data, None)

    def test_project_invalid_details(self):
        detail_data = {
            'versions': ['1.9.0']
        }
        self.assertRaises(SyntaxError, detail.Detail, detail_data)

    def test_project_no_extensions(self):
        data = {
            'name': 'project',
            'type': 'application',
            'vcs': 'svn',
            'url': 'http://subversion',
            'platforms': ['platformx', 'platformy'],
            'options': ['optionx', 'optiony']
        }
        detail_data = {
            'branch': 'brancha',
            'versions': ['1.0', '2.0'],
        }
        p = project.Project(data, detail.Detail(detail_data))
        self.assertEqual(p.name(), 'project')
        self.assertEqual(p.type(), 'application')
        self.assertEqual(p.vcs(), 'svn')
        self.assertEqual(p.url(), 'http://subversion')
        self.assertEqual(p.platforms(), ['platformx', 'platformy'])
        self.assertEqual(p.branch(), 'brancha')
        self.assertEqual(p.versions(), [[1, 0], [2, 0]])
        self.assertEqual(p.dependencies(), [])
        self.assertEqual(p.options(), ['optionx', 'optiony'])

    def test_project_full(self):
        data = {
            'name': 'project',
            'type': 'application',
            'vcs': 'git',
            'url': 'http://github.com/user/project',
            'platforms': ['platformx', 'platformy'],
            'options': ['optiona', 'optionb', 'optionc', 'optiond'],
            'dependencies': ['projecta:=1.0:=2.0:=3.0', 'projectb:<2.0', 'projectc:>3.0:<3.2']
        }
        detail_data = {
            'branch': 'branchb',
            'versions': ['4.0'],
            'includes': {
                'platforms': ['platformz'],
                'options': ['optione', 'optionf', 'optionh'],
                'dependencies': ['projectd:=1.0:=1.1:=1.2:>1.1:<3.0']
            },
            'excludes': {
                'platforms': ['platformy'],
                'options': ['optionb', 'optionc'],
                'dependencies': ['projecta:=2.0', 'projectb']
            }
        }
        p = project.Project(data, detail.Detail(detail_data))
        self.assertEqual(p.name(), 'project')
        self.assertEqual(p.type(), 'application')
        self.assertEqual(p.vcs(), 'git')
        self.assertEqual(p.url(), 'http://github.com/user/project')
        self.assertEqual(p.platforms(), ['platformx', 'platformz'])
        self.assertEqual(p.branch(), 'branchb')
        self.assertEqual(p.versions(), [[4, 0]])
        self.assertEqual(len(p.dependencies()), 3)
        self.assertEqual(p.dependencies()[0].get_name(), 'projecta')
        self.assertEqual(p.dependencies()[0].get_versions(), {'ver': [[1, 0], [3, 0]],
                                                              'min': None,
                                                              'max': None})
        self.assertEqual(p.dependencies()[1].get_name(), 'projectc')
        self.assertEqual(p.dependencies()[1].get_versions(), {'ver': [],
                                                              'min': [3, 0],
                                                              'max': [3, 2]})
        self.assertEqual(p.dependencies()[2].get_name(), 'projectd')
        self.assertEqual(p.dependencies()[2].get_versions(), {'ver': [[1, 0], [1, 1], [1, 2]],
                                                              'min': [1, 1],
                                                              'max': [3, 0]})
        self.assertEqual(p.options(), ['optiona', 'optiond', 'optione', 'optionf', 'optionh'])

    def test_branch_and_versions_replace(self):
        data = {
            'name': 'libx',
            'type': 'library',
            'vcs': 'hg',
            'url': 'http://mercutial',
            'platforms': ['platforma'],
            'branch': 'branch_default',
            'versions': ['1.0.0.0']
        }
        detail_data = {
            'branch': 'branchx',
            'versions': ['1.0.1.0', '1.0.2.0']
        }
        p = project.Project(data, detail.Detail(detail_data))
        self.assertEqual(p.name(), 'libx')
        self.assertEqual(p.type(), 'library')
        self.assertEqual(p.vcs(), 'hg')
        self.assertEqual(p.url(), 'http://mercutial')
        self.assertEqual(p.platforms(), ['platforma'])
        self.assertEqual(p.branch(), 'branchx')
        self.assertEqual(p.versions(), [[1, 0, 0, 0], [1, 0, 1, 0], [1, 0, 2, 0]])
        self.assertEqual(p.dependencies(), [])
        self.assertEqual(p.options(), [])

if __name__ == '__main__':
    unittest.main()
