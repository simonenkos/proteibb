from proteibb.core.properties import *

class Branch(Property.Handler):

    def __init__(self, data):
        properties = [
            StringProperty('name', is_optional=False),
            VersionProperty(is_optional=True),
            PropertyListAdapter('platforms', True, ExtensionAdapter, '', StringProperty),
            PropertyListAdapter('options', True, ExtensionAdapter, '', StringProperty),
            PropertyListAdapter('dependencies', True, ExtensionAdapter, '', DependencyProperty),
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def version(self):
        pass

    @Property.Handler.replace
    def platforms(self):
        pass

    @Property.Handler.replace
    def options(self):
        pass

    @Property.Handler.replace
    def dependencies(self):
        pass
