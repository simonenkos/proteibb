from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import StringsListProperty
from proteibb.util.simple_factory import register_at_factory
from proteibb.core.project.details import details_factory

@register_at_factory(details_factory)
class Application(PropertyHandler):
    """
    Additional options for project details which depends on project type:
    "platforms" : [
        "arm",
        "x86",
        ...
    ]
    "options" : [
        "option_support_feature_x",
        "option_support_feature_y",
        "option_disable_feature_z",
        ...
    ]
    """
    def __init__(self, data):
        properties = [
            StringsListProperty('platforms'),
            StringsListProperty('options')
        ]
        PropertyHandler.__init__(self, properties, data)

    @PropertyHandler.replace
    def platforms(self):
        pass

    @PropertyHandler.replace
    def options(self):
        pass
