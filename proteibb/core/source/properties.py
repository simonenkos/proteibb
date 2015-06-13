from proteibb.util import *
from dependency import *

import rfc3987
import re

class SourceProperty(Property):

    def __init__(self, name, default_value, is_optional=False, is_detail_specific=False):
        Property.__init__(self, name, default_value, is_optional)
        self._is_detail_specific = is_detail_specific

    def is_detail_specific(self):
        return self._is_detail_specific

class StringProperty(SourceProperty):

    def __init__(self, string, is_optional=False, is_detail_specific=False):
        SourceProperty.__init__(self, string, "", is_optional, is_detail_specific)
        self._set_validator(lambda val: isinstance(val, str))

class UrlProperty(SourceProperty):

    def __init__(self):
        SourceProperty.__init__(self, 'url', "")
        self._set_validator(lambda val: isinstance(val, str) and len(val) and rfc3987.match(val, 'URI') is not None)

class VcsProperty(SourceProperty):

    def __init__(self):
        SourceProperty.__init__(self, 'vcs', "")
        self._set_validator(lambda val: isinstance(val, str) and len(val) and val in ['svn', 'git', 'hg'])

class VersionProperty(SourceProperty):

    def __init__(self):
        SourceProperty.__init__(self, 'version', [], True, True)
        validate = lambda val: isinstance(val, str) and (not len(val) or re.match('^(?:\d+)(?:\.\d+)*$', val))
        self._set_validator(validate)

    def _apply_new_value(self, value):
        version = []
        if len(value):
            version = split_version(value)
        SourceProperty._apply_new_value(self, version)

class DependenciesProperty(SourceProperty):

    def __init__(self):
        SourceProperty.__init__(self, 'dependencies', [], True, True)

        def validate(val):
            if not isinstance(val, list):
                return False
            for dep in val:
                if not isinstance(dep, str) or not re.match('^(?:\w+)(?:(?::(?:=|>|<)\d+)(?:\.\d+)*)*$', dep):
                    return False
            return True

        self._set_validator(validate)

    def _apply_new_value(self, dep_list):
        dependencies = []
        for dep in dep_list:
            dep_details = dep.split(':')
            d = Dependency(dep_details[0])
            for version in dep_details[1:]:
                v = split_version(version[1:])
                q = version[0]
                d.add_version(v, q)
            dependencies.append(d)
        SourceProperty._apply_new_value(self, dependencies)
