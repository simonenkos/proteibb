import json

from os import listdir
from os.path import isfile, join, splitext

from proteibb.core.project.project import Project
from proteibb.core.source import source_factory

class Workspace:
    """
    This class loads a structure of the build system into
    a set of projects, sources and configurations.
    """

    workspace_structure = ['configuration', 'projects', 'sources']

    def __init__(self, base_path):
        self._configuration = None
        self._projects = []
        self._sources = []

        if not base_path.endwith('/'):
            base_path.append('/')

        for structure in self.workspace_structure:
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
                    creation_callback(entry_data)

    def _add_configuration(self, data):
        self._configuration = Configuration(data)

    def _add_projects(self, data):
        project = Project(data)
        project.setup(self._configuration, self._sources)
        self._projects.append(project)

    def _add_sources(self, data):
        sources = source_factory.make(data)
        self._sources.append(sources)

    def get_projects(self, project_filter):
        return project_filter(self._projects)

    def get_sources(self, source_filter):
        return source_filter(self._sources)
