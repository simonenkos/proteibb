import unittest

from proteibb.core.project import project

class ProjectTestCase(unittest.TestCase):

    # def test_project_no_data(self):
    #     data = {}
    #     self.assertRaises(SyntaxError, project.Project, data)
    #
    # def test_project_incomplete_data(self):
    #     data = {
    #         'name': 'project',
    #         'type': 'library',
    #     }
    #     self.assertRaises(SyntaxError, project.Project, data)
    #
    # def test_project_no_branch_data(self):
    #     data = {
    #         'name': 'project',
    #         'type': 'library',
    #         'vcs': 'git',
    #         'url': 'http://gitblit',
    #         'platforms': ['platformx', 'platformy'],
    #     }
    #     self.assertRaises(SyntaxError, project.Project, data)
    #
    # def test_project_empty_branch_data(self):
    #     data = {
    #         'name': 'project',
    #         'type': 'library',
    #         'vcs': 'git',
    #         'url': 'http://gitblit',
    #         'platforms': ['platformx', 'platformy'],
    #         'branches': []
    #     }
    #     self.assertRaises(SyntaxError, project.Project, data)
    #
    # def test_project_incomplete_branch_data(self):
    #     data = {
    #         'name': 'project',
    #         'type': 'library',
    #         'vcs': 'git',
    #         'url': 'http://gitblit',
    #         'platforms': ['platformx', 'platformy'],
    #         'branches': [
    #             {
    #                 'version': '1.2'
    #             }
    #         ]
    #     }
    #     self.assertRaises(SyntaxError, project.Project, data)
    #
    # def test_project_complete_data_simple(self):
    #     data = {
    #         'name': 'project',
    #         'type': 'library',
    #         'vcs': 'git',
    #         'url': 'http://gitblit',
    #         'branches': [
    #             {
    #                 'name': 'master',
    #                 'version': '0.7'
    #             }
    #         ]
    #     }
    #     p = project.Project(data)
    #     self.assertEqual(p.name(), 'project')
    #     self.assertEqual(p.type(), 'library')
    #     self.assertEqual(p.vcs(), 'git')
    #     self.assertEqual(p.url(), 'http://gitblit')
    #     self.assertEqual(len(p.branches()), 1)
    #     self.assertEqual(p.branches()[0].name(), 'master')
    #     self.assertEqual(p.branches()[0].version(), [0, 7])

    def test_project_complete_data_full(self):
        data = {
            'name': 'project',
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
                'lib_a:1.0:1.1:1.2:1.3',
                'lib_b:3.0.17.6',
                'lib_c:2.0',
                'lib_d:1.0:1.5'
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
                        '+lib_e:4.3.2',
                        '+lib_a:1.4'
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
                        '-lib_b:3.0.17.6',
                        '+lib_b:3.0.15.1',
                        '-lib_a:1.3:1.2'
                    ]
                },
                {
                    'name': 'release_2',
                    'version': '2.1',
                    'dependencies': [
                        '-lib_d:1.5',
                        '+lib_d:1.2:1.3:1.4'
                    ]
                }
            ]
        }
        p = project.Project(data)
        self.assertEqual(p.name(), 'project')
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
        bd = b[0].dependencies(p)
        self.assertEqual(len(bd), 5)
        self.assertEqual(bd[0].get_name(), 'lib_a')
        self.assertEqual(bd[0].get_versions(), [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4]])
        self.assertEqual(bd[1].get_name(), 'lib_b')
        self.assertEqual(bd[1].get_versions(), [[3, 0, 17, 6]])
        self.assertEqual(bd[2].get_name(), 'lib_c')
        self.assertEqual(bd[2].get_versions(), [[2, 0]])
        self.assertEqual(bd[3].get_name(), 'lib_d')
        self.assertEqual(bd[3].get_versions(), [[1, 0], [1, 5]])
        self.assertEqual(bd[4].get_name(), 'lib_e')
        self.assertEqual(bd[4].get_versions(), [[4, 3, 2]])
        # second branch
        self.assertEqual(b[1].name(), 'release_1')
        self.assertEqual(b[1].version(), [1, 3])
        self.assertEqual(b[1].platforms(p), ['x86'])
        self.assertEqual(b[1].options(p), ['option_a', 'option_b'])
        bd = b[1].dependencies(p)
        self.assertEqual(len(bd), 2)
        self.assertEqual(bd[0].get_name(), 'lib_a')
        self.assertEqual(bd[0].get_versions(), [[1, 0], [1, 1]])
        self.assertEqual(bd[1].get_name(), 'lib_b')
        self.assertEqual(bd[1].get_versions(), [[3, 0, 15, 1]])
        # third branch
        self.assertEqual(b[2].name(), 'release_2')
        self.assertEqual(b[2].version(), [2, 1])
        self.assertEqual(b[2].platforms(p), ['x86', 'arm'])
        self.assertEqual(b[2].options(p), ['option_a', 'option_b', 'option_c', 'option_d'])
        bd = b[2].dependencies(p)
        self.assertEqual(len(bd), 4)
        self.assertEqual(bd[0].get_name(), 'lib_a')
        self.assertEqual(bd[0].get_versions(), [[1, 0], [1, 1], [1, 2], [1, 3]])
        self.assertEqual(bd[1].get_name(), 'lib_b')
        self.assertEqual(bd[1].get_versions(), [[3, 0, 17, 6]])
        self.assertEqual(bd[2].get_name(), 'lib_c')
        self.assertEqual(bd[2].get_versions(), [[2, 0]])
        self.assertEqual(bd[3].get_name(), 'lib_d')
        self.assertEqual(bd[3].get_versions(), [[1, 0], [1, 2], [1, 3], [1, 4]])

if __name__ == '__main__':
    unittest.main()
