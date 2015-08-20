import unittest

from proteibb.core.project import project


class ProjectTestCase(unittest.TestCase):

    def test_project_no_data(self):
        data = {}
        self.assertRaises(SyntaxError, project.Project, data)

    def test_project_incomplete_data(self):
        data = {
            'name': 'Library A',
            'type': 'library',
        }
        self.assertRaises(SyntaxError, project.Project, data)

    def test_project_no_branch_data(self):
        data = {
            'name': 'Library A',
            'code': 'library-a',
            'type': 'library',
            'vcs': 'git',
            'url': 'http://gitblit',
            'platforms': ['platformx', 'platformy'],
        }
        self.assertRaises(SyntaxError, project.Project, data)

    def test_project_empty_branch_data(self):
        data = {
            'name': 'Library A',
            'code': 'library-a',
            'type': 'library',
            'vcs': 'git',
            'url': 'http://gitblit',
            'platforms': ['platformx', 'platformy'],
            'branches': []
        }
        self.assertRaises(SyntaxError, project.Project, data)

    def test_project_incomplete_branch_data(self):
        data = {
            'name': 'Library A',
            'code': 'library-a',
            'type': 'library',
            'vcs': 'git',
            'url': 'http://gitblit',
            'platforms': ['platformx', 'platformy'],
            'branches': [
                {
                    'version': '1.2'
                }
            ]
        }
        self.assertRaises(SyntaxError, project.Project, data)

    def test_project_complete_data_simple(self):
        data = {
            'name': 'Library A',
            'code': 'library-a',
            'type': 'library',
            'vcs': 'git',
            'url': 'http://gitblit',
            'branches': [
                {
                    'name': 'master',
                    'version': '0.7'
                }
            ]
        }
        p = project.Project(data)
        self.assertEqual(p.name(), 'Library A')
        self.assertEqual(p.code(), 'library-a')
        self.assertEqual(p.type(), 'library')
        self.assertEqual(p.vcs(), 'git')
        self.assertEqual(p.url(), 'http://gitblit')
        self.assertEqual(len(p.branches()), 1)
        self.assertEqual(p.branches()[0].name(), 'master')
        self.assertEqual(p.branches()[0].version(), [0, 7])

    def test_project_complete_data_full(self):
        data = {
            'name': 'Project X',
            'code': 'projectx',
            'type': 'application',
            'vcs': 'svn',
            'url': 'http://subversion',
            'platforms': [
                'x86',
                'arm'
            ],
            'options': [
                'option_a',
                'option_b',
                'option_c',
                'option_d'
            ],
            'dependencies': [
                'lib_a',
                'lib_b',
                'lib_c',
                'lib_d'
            ],
            'branches': [
                {
                    'name': 'trunk',
                    'version': '2.7',
                    'options': [
                        '-option_b',
                        '-option_d',
                        '+option_x',
                        '+option_y'
                    ],
                    'dependencies': [
                        '+lib_e',
                    ]
                },
                {
                    'name': 'release_1',
                    'version': '1.3',
                    'platforms': [
                        '-arm'
                    ],
                    'options': [
                        '-option_c',
                        '-option_d'
                    ],
                    'dependencies': [
                        '-lib_d',
                        '-lib_c',
                        '-lib_a'
                    ]
                },
                {
                    'name': 'release_2',
                    'version': '2.1',
                    'dependencies': [
                        '-lib_d',
                        '+lib_d'
                    ]
                }
            ]
        }
        p = project.Project(data)
        self.assertEqual(p.name(), 'Project X')
        self.assertEqual(p.code(), 'projectx')
        self.assertEqual(p.type(), 'application')
        self.assertEqual(p.vcs(), 'svn')
        self.assertEqual(p.url(), 'http://subversion')
        b = p.branches()
        self.assertEqual(len(b), 3)
        # first branch
        self.assertEqual(b[0].name(), 'trunk')
        self.assertEqual(b[0].version(), [2, 7])
        self.assertEqual(b[0].platforms(p), ['x86', 'arm'])
        self.assertEqual(b[0].options(p), ['option_a', 'option_c', 'option_x', 'option_y'])
        self.assertEqual(b[0].dependencies(p), ['lib_a', 'lib_b', 'lib_c', 'lib_d', 'lib_e'])
        # second branch
        self.assertEqual(b[1].name(), 'release_1')
        self.assertEqual(b[1].version(), [1, 3])
        self.assertEqual(b[1].platforms(p), ['x86'])
        self.assertEqual(b[1].options(p), ['option_a', 'option_b'])
        self.assertEqual(b[1].dependencies(p), ['lib_b'])
        # third branch
        self.assertEqual(b[2].name(), 'release_2')
        self.assertEqual(b[2].version(), [2, 1])
        self.assertEqual(b[2].platforms(p), ['x86', 'arm'])
        self.assertEqual(b[2].options(p), ['option_a', 'option_b', 'option_c', 'option_d'])
        self.assertEqual(b[2].dependencies(p), ['lib_a', 'lib_b', 'lib_c', 'lib_d'])

if __name__ == '__main__':
    unittest.main()
