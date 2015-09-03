from proteibb.core.properties import *
from proteibb.core.configuration.slave import Slave
from proteibb.core.configuration import configuration_factory
from proteibb.util.factory import register_class


@register_class(configuration_factory)
class General(Property.Handler):
    """
    Example of general.json file which keeps general information about build system:
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
            StringProperty('svnuser', True),
            StringProperty('svnpass', True),
            PropertyListAdapter('slaves', False, SubProperty, PropertyAdapter.Arguments(False, Slave))
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
