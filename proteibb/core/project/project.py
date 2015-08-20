from proteibb.core.properties import *
from proteibb.core.project.branch import Branch


class Project(Property.Handler):
    """
    Example of project configuration json file:
    {
        "code" : "project_unique_code",
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
            "projectx",
            "projecty",
            "projectz"
        ],
        // Common options list (for application type only).
        "options" : [
            "option_support_feature_x",
            "option_support_feature_y",
            "option_disable_feature_z",
            ...
        ],
        // This section describes branches of a project.
        "branches" : [
            {
                "name" : "branch_x",
                "version" : "x.y.z",
                "platforms" : [
                    "+mips"
                ],
                "options" : [
                    "+option_disable_fix_a",
                    "+option_enable_fix_b",
                    "-option_disable_feature_z"
                ],
                "dependencies" : [
                    "-projectz",
                    "+projecta"

                ]
            },
            {
                "name" : 'branch_z",
                "version" : "a.b.c",
            },
        ]
    }
    """
    def __init__(self, data):
        properties = [
            StringProperty('code'),
            StringProperty('name'),
            TypeProperty(),
            VcsProperty(),
            UrlProperty(),
            ExtensionPropertyListAdapter('platforms', True, StringProperty),
            ExtensionPropertyListAdapter('dependencies', True, StringProperty),
            ExtensionPropertyListAdapter('options', True, StringProperty),
            PropertyListAdapter('branches', False, SubProperty, PropertyAdapter.Arguments(False, Branch))
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def code(self):
        pass

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def type(self):
        pass

    @Property.Handler.replace
    def vcs(self):
        pass

    @Property.Handler.replace
    def url(self):
        pass

    @Property.Handler.replace
    def branches(self):
        pass
