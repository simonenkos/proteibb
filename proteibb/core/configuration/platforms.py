from proteibb.util.simple_factory import *

class Platforms:
    """
    Example of platfroms.json configuration file:
    {
        "platforma" : { builder-dependent-platforma-info },
        "platformb" : { builder-dependent-platformb-info },
    }
    """
    def __init__(self, data, platform_factory):
        if not isinstance(data, dict):
            raise SyntaxError("invalid 'platforms.json' structure")
        if not isinstance(platform_factory, SimpleFactory):
            raise TypeError("invalid platform factory provided")
        self._platforms = {}
        for platform_name, platform_data in data.items():
            self._platforms[platform_name] = platform_factory.make(platform_data)

    def get_platform(self, platform_name):
        return self._platforms[platform_name]
