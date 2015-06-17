from proteibb.core.source import source as src
from proteibb.core.source import source_factory
from proteibb.util.simple_factory import register_at_factory

@register_at_factory(source_factory)
class Production(src.Source):

    def __init__(self, data, details):
        src.Source.__init__(self, data, details)

    def get_change_source(self, configuration):
        return None

    def get_sources(self):
        raise NotImplementedError()
