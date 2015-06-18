from proteibb.core.project.properties import *
from proteibb.core.project.details import details_factory
from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import StringProperty, StringsListProperty

# Register detail at factory.
from proteibb.core.project.details.application import Application

class ProjectSetupError(Exception):
    pass

class Project(PropertyHandler):

    """
    Example of project configuration json file:
    {
        "name" : "project",
        "type" : "library|application|test",
        "vcs"  : "svn|git|hg",
        "url"  : "http://url_to_repository",
        "branches" : [
            "branch-name-one",
            "default-branch"
        ],
        "versions" : [
            "a.b.c",
            "a.b.d"
        ],
        "dependencies" : [
            "projectx:=a.b",
            "projecty",
            "projectz:>3.0"
        ],
        // Options for project details.
    }
    """

    def __init__(self, data):
        properties = [
            StringProperty('name'),
            TypeProperty(),
            VcsProperty(),
            UrlProperty(),
            StringsListProperty('branches', True),
            VersionsProperty(),
            DependenciesProperty()
        ]
        PropertyHandler.__init__(self, properties, data)
        self._details = details_factory.make(self.type().get_value(), data)
        self._source_hierarchy = None

    @PropertyHandler.replace
    def name(self):
        pass

    @PropertyHandler.replace
    def type(self):
        pass

    @PropertyHandler.replace
    def vcs(self):
        pass

    @PropertyHandler.replace
    def url(self):
        pass

    @PropertyHandler.replace
    def branches(self):
        pass

    @PropertyHandler.replace
    def versions(self):
        pass

    @PropertyHandler.replace
    def dependencies(self):
        pass
