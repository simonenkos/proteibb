from proteibb.core.source import source as src
from proteibb.core.source import source_factory
from proteibb.util.simple_factory import register_at_factory

@register_at_factory(source_factory)
class Automation(src.Source):

    def __init__(self, data, details):
        src.Source.__init__(self, data, details)

    def get_change_source(self, configuration):
        cs = self.vcs().get_value()
        getattr(self, '_' + cs + '_change_source')(configuration)

    def _svn_change_source(self, configuration):
        pass

    def _git_change_source(self, configuration):
        pass

    def _hg_change_source(self, configuration):
        pass
