from proteibb.core.source import source as src
from proteibb.core.source import add_source_factory

@add_source_factory
class Automation(src.Source):

    def __init__(self, data, details):
        src.Source.__init__(self, data, details)

    def get_change_source(self):
        raise NotImplementedError()

    # def get_change_source(self, configuration):
    #     vcs = self.get('vcs')
    #     if vcs is 'svn':
    #
    #     pass