from proteibb.core.properties import *

class ProjectSetupError(Exception):
    pass

class Project(Property.Handler):
    """
    Example of project configuration json file:
    {
        "name" : "project",
        "type" : "library|application|test",
        "vcs"  : "svn|git|hg",
        "url"  : "http://url_to_repository",
        // Optional version information for dependency resolving.
        "version" : "a.b.c",
        // Optional default branch name, which can be overwritten in details.
        "branch" : "default_branch",
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
        // Options for project details.
        // It's optional section, but if provided it extends default properties.
        // There are may be multiple details for which multiple projects will be created.
        "details" : [
            {
                "branch" : "branch_x", // Not optional.
                "includes" : {
                    "platforms" : [
                        "mips"
                    ],
                    "options" : [
                        "option_disable_fix_a"
                    ],
                    "dependencies" : [
                        "projectq:a.b.c.d.e"
                    ]
                }
                "excludes" : {
                    // Same as 'includes' section.
                }
            },
            {
                "branch" : 'branch_z",
                "version" : "x.y.z.w"
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
            VersionProperty(is_optional=True),
            StringProperty('branch', is_optional=True),
            PropertyListAdapter(StringProperty, 'platforms', is_optional=True),
            PropertyListAdapter(DependencyProperty, 'dependencies', is_optional=True),
            PropertyListAdapter(StringProperty, 'options', is_optional=True)
        ]
        Property.Handler.__init__(self, properties, data)
        # Customize current project according to specific details.
        if not detail:
            raise SyntaxError('invalid section of project details')
        detail.modify(self._properties)

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
    def platforms(self):
        pass

    @Property.Handler.replace
    def branch(self):
        pass

    @Property.Handler.replace
    def version(self):
        pass

    @Property.Handler.replace
    def dependencies(self):
        pass

    @Property.Handler.replace
    def options(self):
        pass
