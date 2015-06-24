from proteibb.core.properties import *

class Option(Property.Handler):

    def __init__(self, data):
        properties = [
            StringProperty('name', is_optional=False),
            StringProperty('branch', is_optional=True)
        ]
        Property.Handler.__init__(self, properties, data)

    def get_name(self):
        return self._name

    def get_data(self):
        return self._data

class OptionGroup:

    def __init__(self):
        pass