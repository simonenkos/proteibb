from proteibb.core.properties import *
from proteibb.core.options import OptionsGroup
from proteibb.core.platforms import PlatformsGroup

class Builder(Property.Handler):
    """
    Example of builder json configuration file:
    {
        "name" : "builder-name",
        "options" : { ... },
        "platforms" : [ ... ],
    }
    This class describes a base structure of a builder. Successors of this class should
    implement specific properties of a concrete builder in addition to existing ones.
    """
    def __init__(self, data, options_factory, platforms_factory):
        properties = [
            StringProperty('name'),
            GroupProperty('options', False, OptionsGroup, options_factory),
            GroupProperty('platforms', True, PlatformsGroup, platforms_factory)
        ]
        Property.Handler.__init__(self, properties, data)
