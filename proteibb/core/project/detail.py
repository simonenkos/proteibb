from proteibb.core.project.properties import *
from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import *

class Detail(PropertyHandler):

    class Extensions(PropertyHandler):

        def __init__(self, data):
            properties = [
                StringsListProperty('platforms', is_optional=True),
                StringsListProperty('options', is_optional=True),
                DependenciesProperty()
            ]
            PropertyHandler.__init__(self, properties, data)

    def __init__(self, data):
        properties = [
            StringProperty('branch', is_optional=False),
            VersionsProperty(),
            ExtensionsProperty('includes', Detail.Extensions),
            ExtensionsProperty('excludes', Detail.Extensions),
        ]
        PropertyHandler.__init__(self, properties, data)

    def modify(self, properties_map):
        def set_extensions(name, change_policy):
            ext = self._properties[name].get_value()
            if ext:
                ext.apply_change_policy(properties_map, change_policy)
        self.apply_change_policy(properties_map, include_property_value)
        set_extensions('includes', include_property_value)
        set_extensions('excludes', exclude_property_value)

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
