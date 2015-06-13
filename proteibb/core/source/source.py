from properties import *

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
                "dependencies : [ "lib_a:=0.0.5:=0.0.6:=0.0.7:=0.0.8" ]
                // production-specific options
            },
            {
                "branch"  : "release_1_1",
                "version" : "1.1"
                "dependencies" : [ "lib_a:>0.0.9:<0.1.9", "lib_b:=1.1", "lib_c" ],
            },
        ],
        "user" : [
            {
                "branch" : "new_feature_1",
                "version" : "1.3",
                // user-specific options
                "dep-branch" : "trunk",
                "dependencies" : [ "lib_d:>1.0" ]

            }
        ],
    }
    A version of software code is an optional parameter.
    Dependencies lists are also optional.
    """

    def __init__(self, data, details):
        prop_list = [
            StringProperty('name'),
            VcsProperty(),
            UrlProperty(),
            StringProperty('branch', True, True),
            StringProperty('revision', False, True),
            VersionProperty(),
            DependenciesProperty(),
        ]
        self._properties = {}
        for prop in prop_list:
            self._properties[prop.get_name()] = prop

    def get_property(self, property_name):
        return self._properties[property_name]

    # def get_name(self):
    #     return self._properties['name']
    #
    # def get_vcs(self):
    #     return self._properties['vcs']
    #
    # def get_url(self):
    #     return self._url
    #
    # def get_branch(self):
    #     return self._branch
    #
    # def get_version(self):
    #     return self._version
    #
    # def get_dependencies(self):
    #     return self._dependencies

    def get_change_source(self):
        raise NotImplementedError()

    def get_sources(self):
        raise NotImplementedError()
