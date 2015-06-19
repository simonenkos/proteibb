from proteibb.core.project.properties import *
from proteibb.util.property_handler import PropertyHandler
from proteibb.util.property import StringProperty, StringsListProperty

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
        // Common platforms list.
        "platforms" : [
            "arm",
            "x86",
            ...
        ],
        // Common dependencies list.
        "dependencies" : [
            "projectx:=a.b",
            "projecty",
            "projectz:>c.d"
        ],
        // Common options list (for application type only).
        "options" : [
            "option_support_feature_x",
            "option_support_feature_y",
            "option_disable_feature_z",
            ...
        ],
        // Options for project details.
        "details" : [
            {
                "branch" : "branch_x",
                "versions" : [
                    "a.b.c",
                    "d.e.f"
                ],
                "includes" : {
                    "platforms" : [
                        "mips"
                    ],
                    "options" : [
                        "option_disable_fix_a"
                    ],
                    "dependencies" : [
                        "projectq:<a.b.c.d.e"
                    ]
                }
                "excludes" : {
                    // Same as 'includes' section.
                }
            },
            {
                "branch" : 'branch_z",
                "versions" : [
                    "a.b.c"
                ]
            },
        ]
    }
    """
    def __init__(self, data, detail):
        properties = [
            StringProperty('name'),
            TypeProperty(),
            VcsProperty(),
            UrlProperty(),
            StringsListProperty('platforms'),
            StringProperty('branch', True),
            VersionsProperty(),
            DependenciesProperty(),
            StringsListProperty('options', True)
        ]
        PropertyHandler.__init__(self, properties, data)
        # Customize current project according to specific details.
        detail.modify(self._properties)

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
    def platforms(self):
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

    @PropertyHandler.replace
    def options(self):
        pass
