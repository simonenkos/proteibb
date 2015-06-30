from proteibb.core.properties import *

class Configuration(Property.Handler):
    """
    Example of configuration.json file which keeps general information about build system:
    {
        "svnuser" : "username",
        "svnpass" : "userpassword",
        "builder" : "builder-name"
    }
    """
    def __init__(self, data):
        properties = [
            StringProperty('svnuser'),
            StringProperty('svnpass'),
            StringProperty('builder')
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def svnuser(self):
        pass

    @Property.Handler.replace
    def svnpass(self):
        pass

    @Property.Handler.replace
    def builder(self):
        pass
