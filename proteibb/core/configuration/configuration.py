from proteibb.core.properties import *
from proteibb.core.configuration.slave import Slave


class Configuration(Property.Handler):
    """
    Example of configuration.json file which keeps general information about build system:
    {
        "svnuser" : "user-name",
        "svnpass" : "user-password",
        "slaves"  : [
            {
                "name" : "slave-x",
                "pass" : "slave-x-password",
            },
        ]
    }
    """
    def __init__(self, data):
        properties = [
            StringProperty('svnuser'),
            StringProperty('svnpass'),
            PropertyListAdapter('slaves', False, SubProperty, PropertyAdapter.Arguments(Slave))
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def svnuser(self):
        pass

    @Property.Handler.replace
    def svnpass(self):
        pass

    @Property.Handler.replace
    def slaves(self):
        pass
