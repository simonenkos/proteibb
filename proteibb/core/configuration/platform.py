from proteibb.core.properties import *

class Platform(Property.Handler):

    def __init__(self, data):
        properties = [
            
        ]
        Property.Handler.__init__(self, properties, data)

    def get_name(self):
        return self._name

    def get_options(self):
        return self._options
