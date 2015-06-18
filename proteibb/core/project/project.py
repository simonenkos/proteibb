# from proteibb.core.project.properties import PlatformsProperty
from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import StringProperty, StringsListProperty

class ProjectSetupError(Exception):
    pass

class Project(PropertyHandler):

    """
    Example of project configuration json file:
    {
        "name" : "project",
        "source" : "project_source_name"
        // Common properties.
        "platforms" : [
           "arm",
           "x86",
        ]
        // Configuration options for user and productions builds.
        "options" : [
            "option_support_feature_x",
            "option_support_feature_y",
            "option_disable_feature_z",
            // Other options.
        ]
    }
    """

    def __init__(self, data):
        PropertyHandler.__init__(self)
        # Set up values of properties from configuration.
        for prop_name, prop in self._properties.items():
            prop.set_value(data[prop_name])
        self._source_hierarchy = None

    @PropertyHandler.declare_property(StringProperty, True)
    def name(self):
        pass

    @PropertyHandler.declare_property(StringProperty, True)
    def source(self):
        pass

    @PropertyHandler.declare_property(StringsListProperty, True)
    def platforms(self):
        pass

    @PropertyHandler.declare_property(StringsListProperty, True)
    def options(self):
        pass

    def setup(self, configuration, sources):
        src = filter(lambda s: s.get_name() == self.source(), sources)
        if not src:
            raise ProjectSetupError("source for the project was not found")
        if len(src) > 1:
            raise ProjectSetupError("not single source was found for the project")
