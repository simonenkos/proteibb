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
            'url': 'http://github.com/user/project'
        }
        p = project.Project(data)
        self.assertEqual(p.name().get_value(), 'project')
        self.assertEqual(p.type().get_value(), 'library')
        self.assertEqual(p.vcs().get_value(), 'git')
        self.assertEqual(p.url().get_value(), 'http://github.com/user/project')
        self.assertEqual(p.branches().get_value(), [])
        self.assertEqual(p.versions().get_value(), [])
        self.assertEqual(p.dependencies().get_value(), [])

    def test_project_application_empty_details(self):
        data = {
            'name': 'project',
            'type': 'library',
            'vcs': 'git',
            'url': 'http://github.com/user/project',
            'branches': ['default'],
            'versions': ['1.0', '2.0'],
            'platforms': ['platformx', 'platformy'],
            'options': ['optionx', 'optiony']
        }
        p = project.Project(data)
        # ToDo

if __name__ == '__main__':
    unittest.main()
