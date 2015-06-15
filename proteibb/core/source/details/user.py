from proteibb.core.source import source as src
from proteibb.core.source import add_source_factory
from proteibb.core.source.properties import StringProperty
from proteibb.util.property_handler import PropertyHandler

@add_source_factory
class User(src.Source):

    def __init__(self, data, details):
        src.Source.__init__(self, data, details)

    @PropertyHandler.declare_property(StringProperty, is_optional=True, is_detail_specific=True)
    def specification(self):
        pass

    def get_change_source(self):
        return None

    def get_sources(self):
        raise NotImplementedError()