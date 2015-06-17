from proteibb.util.property_handler import PropertyHandler

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
        for prop_name, prop in self._properties:
            value = data[prop_name]
            if not prop.is_optional() and not value:
                raise

    @PropertyHandler.declare_property()
    def name(self):
        pass
