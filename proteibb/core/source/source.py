from proteibb.util import *

class Source:
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
                "dependencies : [ "lib_a:0.0.5:0.0.6:0.0.7:0.0.8" ]
                // production-specific options
            },
            {
                "branch"  : "release_1_1",
                "version" : "1.1"
                "dependencies" : [ "lib_a:>=0.0.9:<0.1.9", "lib_b:1.1", "lib_c" ]
            },
        ],
        "user" : [
            {
                "branch" : "trunk",
                "version" : "1.3"
                // user-specific options
            }
        ],
    }
    A version of software code is an optional parameter.
    Dependencies lists are also optional.
    """

    common_options = [
        Detail('name', ""),
        Detail('url', ""),
        VCS(),
    ]
    specific_options = [
        {'branch': True},
        {'version': True},
        {'dependencies': True}
    ]

    def __init__(self):
        self._name = ""
        self._vcs = ""
        self._url = ""
        self._branch = ""
        self._version = ""
        self._dependencies = []

    def get_name(self):
        return self._name

    def get_vcs(self):
        return self._vcs

    def get_url(self):
        return self._url

    def get_branch(self):
        return self._branch

    def get_version(self):
        return self._version

    def get_dependencies(self):
        return self._dependencies

    def get_change_source(self):
        raise NotImplementedError()

    def get_sources(self):
        raise NotImplementedError()

    def parse_common_source_details(self, details, detail_names):
        def get_attribute(optional, attr_name):
            attr = details[attr_name]
            if not attr and not optional:
                raise SyntaxError("no '" + attr_name + "' attribute found")
        for name, is_optional in detail_names:
            attr_value = get_attribute(is_optional, name)
            setattr(self, '_' + name, attr_value)
