from proteibb.core.source.properties import *
from proteibb.util.property_handler import PropertyHandler

class Source(PropertyHandler):
    """
    Example of source config file:
    {
        "type" : "library|application",
        "vcs"  : "svn|git|hg",
        "url"  : "http://url_to_repository",
        "automation" : [
            {
                "branch"  : "trunk",
                "version" : "1.2"
                // automation-specific options
            }
        ],
        "production" : [
            {
                "branch"  : "release_1_0",
                "version" : "1.0"
                "dependencies : [ "lib_a:=0.0.5:=0.0.6:=0.0.7:=0.0.8" ]
                // production-specific options
            },
            {
                "branch"  : "release_1_1",
                "version" : "1.1"
                "dependencies" : [ "lib_a:>0.0.9:<0.1.9", "lib_b:=1.1", "lib_c" ],
                // production-specific options
            },
        ],
        "user" : [
            {
                "branch" : "new_feature_1",
                "version" : "1.3",
                "dependencies" : [ "lib_d:>1.0" ],
                // user-specific options
            }
        ],
    }
    A version of software code is an optional parameter.
    Dependencies lists are also optional.
    """

    def __init__(self, data, details):
        PropertyHandler.__init__(self)
        # Set up values to properties according to a configuration in 'data' and 'details'.
        for prop_name, prop in self._properties.items():
            if prop.is_detail_specific():
                value = details.get(prop_name, None)
            else:
                value = data.get(prop_name, None)
            prop.set_value(value)

    @PropertyHandler.declare_property(DetailedStringProperty, True, is_optional=False, is_detail_specific=False)
    def name(self):
        pass

    @PropertyHandler.declare_property(VcsProperty)
    def vcs(self):
        pass

    @PropertyHandler.declare_property(UrlProperty)
    def url(self):
        pass

    @PropertyHandler.declare_property(DetailedStringProperty, True)
    def branch(self):
        pass

    @PropertyHandler.declare_property(DetailedStringProperty, True)
    def revision(self):
        pass

    @PropertyHandler.declare_property(VersionsProperty)
    def versions(self):
        pass

    @PropertyHandler.declare_property(DependenciesProperty)
    def dependencies(self):
        pass

    def get_change_source(self, configuration):
        raise NotImplementedError()
