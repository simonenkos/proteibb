from proteibb.core.properties import *
from proteibb.util.factory import *


class PlatformsGroup:
    """
    Example of platforms list which could be used in some json file:
    {
        "platforma" : { builder-dependent-platforma-info },
        "platformb" : { builder-dependent-platformb-info },
    }
    """
    def __init__(self, data, platform_factory):
        if not isinstance(data, dict):
            raise SyntaxError("invalid 'platforms.json' structure")
        if not isinstance(platform_factory, FactoryInterface):
            raise TypeError("invalid platform factory provided")
        self._platforms = {}
        for platform_name, platform_data in data.items():
            self._platforms[platform_name] = platform_factory.make(platform_data)

    def get_platform(self, platform_name):
        if platform_name not in self._platforms:
            raise ValueError('no platform found with name: ' + platform_name)
        return self._platforms[platform_name]


class PlatformBase(Property.Handler):

    def __init__(self, data, additional_properties=None):
        properties = [
            StringProperty('name', is_optional=False),
            PropertyListAdapter('slaves', False, StringProperty),
        ]
        if additional_properties:
            properties.extend(additional_properties)
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def slaves(self):
        pass
