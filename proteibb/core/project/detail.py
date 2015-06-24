from proteibb.core.properties import *

class Detail(Property.Handler):

    class Extensions(Property.Handler):

        def __init__(self, data):
            properties = [
                PropertyListAdapter(StringProperty, 'platforms', is_optional=True),
                PropertyListAdapter(StringProperty, 'options', is_optional=True),
                PropertyListAdapter(DependencyProperty, 'dependencies', is_optional=True)
            ]
            Property.Handler.__init__(self, properties, data)

    def __init__(self, data):
        properties = [
            StringProperty('branch', is_optional=False),
            PropertyListAdapter(VersionProperty, 'versions', is_optional=True),
            ExtensionProperty('includes', Detail.Extensions),
            ExtensionProperty('excludes', Detail.Extensions),
        ]
        Property.Handler.__init__(self, properties, data)

    def modify(self, properties_map):
        def set_extensions(name, change_policy):
            ext = self._properties[name].get_value()
            if ext:
                ext.apply_change_policy(properties_map, change_policy)
        self.apply_change_policy(properties_map, Property.include_value)
        set_extensions('includes', Property.include_value)
        set_extensions('excludes', Property.exclude_value)

def prepare_project_details(data):
    if not data:
        raise SyntaxError("empty or invalid project configuration set")
    details_data = data['details']
    if not details_data:
        raise SyntaxError("empty or invalid project's details configuration set")
    details = []
    for d in details_data:
        details.append(Detail(d))
    return details
