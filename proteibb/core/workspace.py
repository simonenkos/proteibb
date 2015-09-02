import json

from os import listdir
from os.path import isfile, join, splitext

from proteibb.core.project.project import Project
from proteibb.util.factory import FactoryInterface
from proteibb.core.configuration import configuration_factory
from proteibb.core.builder import builder_factory


class Workspace:
    """
    This class loads a structure of the build system into
    a set of projects and a configuration structure.
    """
    def __init__(self, base_path):
        self._configurations = []
        self._builders = []
        self._projects = []

        if not base_path.endswith('/'):
            base_path += '/'

        for structure in ['configuration', 'builders', 'projects']:
            directory = base_path + structure + '/'
            method_name = '_add_' + structure
            method = getattr(self, method_name)
            self._load_workspace(directory, method)

    @staticmethod
    def _load_workspace(directory, creation_callback):
        for file_name in listdir(directory):
            entry_path = join(directory, file_name)
            entry_name, extension = splitext(file_name)
            if isfile(entry_path) and extension == '.json':
                with open(entry_path) as data_file:
                    entry_data = json.load(data_file)
                    creation_callback(entry_name, entry_data)

    def _add_configuration(self, name, data):
        try:
            conf = configuration_factory.make(data, configuration_name=name)
        except FactoryInterface.NoClassRegistered:
            print "No configuration handler found for: " + name
        else:
            self._configurations.append(conf)

    def _add_builders(self, name, data):
        try:
            builder = builder_factory.make(data, builder_name=name)
        except FactoryInterface.NoClassRegistered:
            print "No builder description handler found for: " + name
        else:
            self._builders.append(builder)

    def _add_projects(self, name, data):
        self._projects.append(Project(data))

    def get_configuration(self, configuration_filter):
        return configuration_filter(self._configurations)

    def get_builders(self, builder_filter):
        return builder_filter(self._builders)

    def get_projects(self, project_filter):
        return project_filter(self._projects)
