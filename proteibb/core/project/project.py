from proteibb.core.properties import *
from proteibb.core.project.branch import Branch


class Project(Property.Handler):
    """
    Example of project configuration json file:
    {
        "name" : "project",
        "type" : "library|application|test",
        "vcs"  : "svn|git|hg",
        "url"  : "http://url_to_repository",
        "path" : "path/where/source/code/should/be/stored
        // Common platforms list.
        "platforms" : [
            "arm",
            "x86",
            ...
        ],
        // Common dependencies list.
        "dependencies" : [
            "projectx:a.b",
            "projecty",
            "projectz:c.d.e:x.y.z"
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
                "version" : "a.b.c",
                "platforms" : [
                    "+mips"
                ],
                "options" : [
                    "+option_disable_fix_a",
                    "+option_enable_fix_b",
                    "-option_disable_feature_z"
                ],
                "dependencies" : [
                    "-projectz:c.d.e",
                    "+projecta:x.y.z"

                ]
            },
            {
                "name" : 'branch_z",
                "version" : "x.y.z.w"
            },
        ]
    }
    """
    def __init__(self, data):
        properties = [
            StringProperty('name'),
            TypeProperty(),
            VcsProperty(),
            UrlProperty(),
            StringProperty('path'),
            ExtensionPropertyListAdapter('platforms', True, StringProperty),
            ExtensionPropertyListAdapter('dependencies', True, DependencyProperty),
            ExtensionPropertyListAdapter('options', True, StringProperty),
            PropertyListAdapter('branches', False, SubProperty, PropertyAdapter.Arguments(False, Branch))
        ]
        Property.Handler.__init__(self, properties, data)

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
    def path(self):
        pass

    @Property.Handler.replace
    def branches(self):
        pass
