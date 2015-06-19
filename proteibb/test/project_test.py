import unittest

from proteibb.core.project import project

class ProjectTestCase(unittest.TestCase):

    def test_project_empty(self):
        data = {}
        self.assertRaises(SyntaxError, project.Project, data)

    def test_project_no_optional(self):
        data = {
            'name': 'project',
            'type': 'library',
            'vcs': 'git',
            'url': 'http://github.com/user/project',
            'platforms': ['platformx', 'platformy']
        }
        p = project.Project(data)
        self.assertEqual(p.name(), 'project')
        self.assertEqual(p.type(), 'library')
        self.assertEqual(p.vcs(), 'git')
        self.assertEqual(p.url(), 'http://github.com/user/project')
        self.assertEqual(p.platforms(), ['platformx', 'platformy'])
        self.assertEqual(p.branches(), [])
        self.assertEqual(p.versions(), [])
        self.assertEqual(p.dependencies(), [])
        self.assertEqual(p.options(), [])

    def test_project_application(self):
        data = {
            'name': 'project',
            'type': 'application',
            'vcs': 'svn',
            'url': 'http://subversion',
            'platforms': ['platformx', 'platformy'],
            'branches': ['default'],
            'versions': ['1.0', '2.0'],
            'options': ['optionx', 'optiony']
        }
        p = project.Project(data)
        self.assertEqual(p.name(), 'project')
        self.assertEqual(p.type(), 'application')
        self.assertEqual(p.vcs(), 'svn')
        self.assertEqual(p.url(), 'http://subversion')
        self.assertEqual(p.platforms(), ['platformx', 'platformy'])
        self.assertEqual(p.branches(), ['default'])
        self.assertEqual(p.versions(), [[1, 0], [2, 0]])
        self.assertEqual(p.options(), ['optionx', 'optiony'])

if __name__ == '__main__':
    unittest.main()
