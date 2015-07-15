from proteibb.core.properties import *
from proteibb.core.options import OptionsGroup
from proteibb.core.platforms import PlatformsGroup

class Builder(Property.Handler):
    """
    Example of builder json configuration file:
    {
        "name" : "builder-name",
        "slaves" : [
            "slave_x86_release",
            "slave_x86_debug"
        ],
        "options" : { ... },
        "platforms" : [ ... ],
    }
    This class describes a base structure of a builder. Successors of this class should
    implement specific properties of a concrete builder in addition to existing ones.
    """
    def __init__(self, data, options_factory, platforms_factory):
        properties = [
            StringProperty('name'),
            PropertyListAdapter('slaves', False, StringProperty),
            GroupProperty('options', False, OptionsGroup, options_factory),
            GroupProperty('platforms', True, PlatformsGroup, platforms_factory)
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def slaves(self):
        pass

    @Property.Handler.replace
    def options(self):
        pass

    @Property.Handler.replace
    def platforms(self):
        pass

    def make_step(self, configuration, projects_data):
        raise NotImplementedError()
