from buildbot.plugins import *

from proteibb.core.properties import *


class Slave(Property.Handler):

    def __init__(self, data):
        properties = [
            StringProperty('name'),
            StringProperty('password')
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def password(self):
        pass

    def make(self):
        return buildslave.BuildSlave(self.name(), self.password())

    def __eq__(self, other):
        if isinstance(other, Slave):
            return self.name() == other.name()
        elif isinstance(other, str):
            return self.name() == other
        else:
            raise ValueError('unsupported type was used for comparison of slaves:' + type(other).__name__)
