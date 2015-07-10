from proteibb.util.factory import register_class
from proteibb.core.builder import builder
from proteibb.core.options import OptionBase
from proteibb.core.platforms import PlatformBase
from proteibb.core.builder.implementations.cppbuilder import *

class CppBuilder(builder.Builder):

    def __init__(self, data):
        builder.Builder.__init__(self, data, options_factory, platforms_factory)

@register_class(options_factory)
class Option(OptionBase):

    def __init__(self, data):
        properties = [
            # Todo add more properties
        ]
        OptionBase.__init__(self, data, properties)


@register_class(platforms_factory)
class Platform(PlatformBase):

    def __init__(self, data):
        properties = [
            # Todo add more properties
        ]
        PlatformBase.__init__(self, data, properties)
