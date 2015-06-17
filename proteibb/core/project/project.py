from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import Property, StringProperty

class Project(PropertyHandler):

    """
    Example of project configuration json file:
    {
        "name" : "project",
        "platform" : [
            "arm",
            "x86",
        ]
        "source" : "project_source_name"

    }

    """

    def __init__(self, data):
        PropertyHandler.__init__(self)
        # Set up values of properties from configuration.
        for prop_name, prop in self._properties.items():
            value = data[prop_name]
            if not prop.is_optional() and not value:
                raise

    @PropertyHandler.declare_property(StringProperty, True)
    def name(self):
        pass

    def platform(self):
        pass

    @PropertyHandler.declare_property(StringProperty, True)
    def source(self):
        pass
