import json

from os import listdir
from os.path import isfile, join, basename, splitext

from proteibb.common.project import *

class Workspace:
    """This class loads a structure of the build system into a set of projects."""

    project_type_list = ['automation', 'production', 'user']

    def __init__(self, base_path):
        self._projects = []

        if not base_path.endwith('/'):
            base_path.append('/')

        def make_project_path(pt):
            return base_path + 'workspace' + pt + '/'

        for project_type in self.project_type_list:
            project_dir = make_project_path(project_type)
            for file_name in listdir(project_dir):
                file_path = join(project_dir, file_name)
                if isfile(file_path) and file_path.endswith('.json'):
                    project = self._make_project(file_path, file_name, project_type)
                    self._projects.append(project)

    @staticmethod
    def _make_project(project_path, project_name, project_type):
        with open(project_path) as data_file:
            project_data = json.load(data_file.readall())
            return make_project(project_path, project_name, project_type, project_data)

    def get_projects(self, project_filter):
        return project_filter(self._projects)
