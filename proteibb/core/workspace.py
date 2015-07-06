import json

from os import listdir
from os.path import isfile, join, splitext

from proteibb.core.project.project import Project
from proteibb.core.configuration import conf_factory

class Workspace:
    """
    This class loads a structure of the build system into
    a set of projects and a configuration structure.
    """
    def __init__(self, base_path):
        self._configurations = []
        self._projects = []

        if not base_path.endwith('/'):
            base_path.append('/')

        for structure in ['configuration', 'projects']:
            directory = base_path + structure + '/'
            method_name = '_add_' + structure
            method = getattr(self, method_name)
            self._load_workspace(directory, method)

    @staticmethod
    def _load_workspace(directory, creation_callback):
        for file_name in listdir(directory):
            entry_path = join(directory, file_name)
            entry_name, extension = splitext(file_name)
            if isfile(entry_path) and extension is '.json':
                with open(entry_path) as data_file:
                    entry_data = json.load(data_file)
                    creation_callback(entry_name, entry_data)

    def _add_configuration(self, name, data):
        conf = conf_factory.make(data, conf_name=name)
        self._configurations.append(conf)

    def _add_projects(self, name, data):
        project = Project(data)
        self._projects.append(project)

    def get_configuration(self, configuration_filter):
        return configuration_filter(self._configurations)

    def get_projects(self, project_filter):
        return project_filter(self._projects)
