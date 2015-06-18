import re
import rfc3987

from proteibb.util import split_version
from proteibb.util.property import Property, EnumerationProperty
from proteibb.core.project.dependency import Dependency

# Source properties specializations.

class TypeProperty(EnumerationProperty):

    def __init__(self):
        EnumerationProperty.__init__(self, 'type', ['library', 'application', 'test'])

class UrlProperty(Property):

    def __init__(self):
        Property.__init__(self, 'url', "")
        self._set_validator(lambda val: isinstance(val, str) and len(val) and rfc3987.match(val, 'URI') is not None)

class VcsProperty(EnumerationProperty):

    def __init__(self):
        EnumerationProperty.__init__(self, 'vcs', ['svn', 'git', 'hg'])

class VersionsProperty(Property):

    def __init__(self):
        Property.__init__(self, 'versions', [], True)

        def validate(val):
            if not isinstance(val, list):
                return False
            for version in val:
                if not isinstance(version, str) or not (len(version) and re.match('^(?:\d+)(?:\.\d+)*$', version)):
                    return False
            return True
        self._set_validator(validate)

    def _apply_new_value(self, value):
        version = []
        for v in value:
            version.append(split_version(v))
        Property._apply_new_value(self, version)

class DependenciesProperty(Property):

    def __init__(self):
        Property.__init__(self, 'dependencies', [], True)

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
        Property._apply_new_value(self, dependencies)
