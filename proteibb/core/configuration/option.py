from proteibb.core.properties import *

class Option(Property.Handler):

    def __init__(self, data):
        properties = [
            StringProperty('name', is_optional=False),
            StringProperty('description', is_optional=False),
            PropertyListAdapter(DependencyProperty, 'dependencies', is_optional=True, is_single_versioned=True),
            PropertyListAdapter(StringProperty, 'defines', is_optional=True)
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def description(self):
        pass

    @Property.Handler.replace
    def dependencies(self):
        pass

    @Property.Handler.replace
    def defines(self):
        pass

class OptionGroup:

    def __init__(self, options_list):
        self._options = []
        for option_data in options_list:
            self._options.append(Option(option_data))

    def get_options(self):
        return self._options
