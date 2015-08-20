from proteibb.core.properties import *
from proteibb.util.factory import *


class OptionsGroup:
    """
    Example of options list which could be used in some json file:
    {
        "option-ab-group-name" : [
            {
                "name" : "optiona",
                "description" : "Option A description",
                "dependencies" : ["liba"]
            },
            {
                "name" : "optionb",
                "description" : "Option B description",
                "dependencies" : ["libb", "libc"]
            }
        ],
        "option-x-group-name" : [
            {
                "name" : "optionx",
                "description" : "Option X description"
            }
        ]
    }
    """
    def __init__(self, data, option_factory):
        if not isinstance(data, dict):
            raise SyntaxError("invalid 'options.json' structure")
        if not isinstance(option_factory, FactoryInterface):
            raise TypeError("invalid option factory type")
        self._option_groups = {}
        for group_name, group_options in data.items():
            options = []
            for option_data in group_options:
                options.append(option_factory.make(option_data))
            self._option_groups[group_name] = options

    def get_options(self, group_name):
        return self._option_groups[group_name]


class OptionBase(Property.Handler):

    def __init__(self, data, additional_options=None):
        properties = [
            StringProperty('name', is_optional=False),
            StringProperty('description', is_optional=False),
            PropertyListAdapter('dependencies', True, StringProperty),
        ]
        if additional_options:
            properties.extend(additional_options)
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
