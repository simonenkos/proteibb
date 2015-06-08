from proteibb.util import *

import rfc3987
import re

class StringProperty(Property):

    def __init__(self, str, is_optional=False):
        Property.__init__(str, "", is_optional)
        self._set_validator(lambda val: isinstance(val, str))

class UrlProperty(Property):

    def __init__(self):
        Property.__init__(self, 'url', "")
        self._set_validator(lambda val: isinstance(val, str) and rfc3987.match(val))

class VcsProperty(Property):

    def __init__(self):
        Property.__init__(self, 'vcs', "")
        self._set_validator(lambda val: isinstance(val, str) and (val for val in ['svn', 'git', 'hg']))

class VersionProperty(Property):

    def __init__(self):
        Property.__init__(self, 'version', "", True)
        # ToDo regex to check version
        self._set_validator(lambda val: isinstance(val, str) and re.match('', val))

class DependenciesProperty(Property):

    def __init__(self):
        Property.__init__(self, 'dependencies', [], True)

        def validate(val):
            if not isinstance(val, list):
                return False
            for dep in val:
                # ToDo regex to check dependencies
                if not isinstance(dep, str) or not re.match('', dep):
                    return False
            return True

        self._set_validator(validate)