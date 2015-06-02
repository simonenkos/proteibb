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
            }
        ],
        "production" : [
            {
                "branch"  : "release_1_0",
                "version" : "1.0"
                "dependencies : [ "lib_a:0.0.5:0.0.6:0.0.7:0.0.8" ]
            },
            {
                "branch"  : "release_1_1",
                "version" : "1.1"
                "dependencies" : [ "lib_a:>=0.0.9:<0.1.9", "lib_b:1.1", "lib_c" ]
            },
        ],
        "user" : [
            {
                "self-branch" : "test_bug10001",
                "prod-branch" : "release_1_0" // copy version, dependencies
            }
        ],
    }
    A version of software code is an optional parameter.
    Dependencies lists are also optional.
    """

    def __init__(self):
        self._name = ""
        self._vcs = None
        self._url = ""
        self._automation = []
        self._production = []
        self._user = []

    def get_change_source(self):
        # ToDo
        return None
