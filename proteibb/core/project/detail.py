from proteibb.core.project.properties import *
from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import *

class Detail(PropertyHandler):

    def __init__(self, data):
        properties = [
            StringProperty('branch', True),
            VersionsProperty(),
            # ExtensionProperty('includes'), # ToDo
            # ExtensionProperty('excludes'), # ToDo
        ]
        PropertyHandler.__init__(self, properties, data)

    def modify(self, properties_map):
        self.apply_change_policy(properties_map, include_property_value)

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
