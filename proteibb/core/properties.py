import rfc3987

from proteibb.util import *
from proteibb.util.dependency import *
from proteibb.util.traits import *

# General properties.

class StringProperty(Property):

    def __init__(self, name, is_optional=False, *args, **kwargs):
        Property.__init__(self, name, "", is_optional, *args, **kwargs)
        self._set_validator(lambda val: isinstance(val, str) and len(val))

class EnumerationProperty(Property):

    def __init__(self, name, enumeration, is_optional=False, *args, **kwargs):
        Property.__init__(self, name, "", is_optional, *args, **kwargs)
        if not isinstance(enumeration, list) or not enumeration:
            raise SyntaxError("invalid enumeration for '" + name + "' property")
        self._set_validator(lambda val: val in enumeration)

# Specialized properties.

class TypeProperty(EnumerationProperty):

    def __init__(self, is_optional=False, *args, **kwargs):
        EnumerationProperty.__init__(self, 'type', ['library', 'application', 'test'], is_optional, *args, **kwargs)

class UrlProperty(Property):

    def __init__(self, is_optional=False, *args, **kwargs):
        Property.__init__(self, 'url', "", is_optional, *args, **kwargs)
        self._set_validator(lambda val: isinstance(val, str) and len(val) and rfc3987.match(val, 'URI') is not None)

class VcsProperty(EnumerationProperty):

    def __init__(self, is_optional=False, *args, **kwargs):
        EnumerationProperty.__init__(self, 'vcs', ['svn', 'git', 'hg'], is_optional, *args, **kwargs)

class VersionProperty(Property):

    def __init__(self, is_optional=False, *args, **kwargs):
        Property.__init__(self, 'version', '', is_optional, *args, **kwargs)
        self._set_validator(lambda val: isinstance(val, str) and len(val) and re.match('^(?:\d+)(?:\.\d+)*$', val))

    def _apply_new_value(self, value):
        self._value = split_version(value)

class DependencyProperty(Property):

    def __init__(self, is_optional=False, *args, **kwargs):
        Property.__init__(self, 'dependency', None, is_optional, *args, **kwargs)
        regex_str = '^(?:\w+)(?:(?::\d+)(?:\.\d+)*)*$'
        validator = lambda val: isinstance(val, str) and len(val) and re.match(regex_str, val)
        self._set_validator(validator)

    def _apply_new_value(self, value):
        dep_details = value.split(':')
        self._value = Dependency(dep_details[0])
        for version in dep_details[1:]:
            self._value.add_version(split_version(version))

class SubProperty(Property):

    def __init__(self, name, is_optional, cls, *args, **kwargs):
        if not issubclass(cls, Property.Handler):
            raise TypeError('invalid sub property class type')
        Property.__init__(self, name, None, is_optional, *args, **kwargs)
        self._sub_cls = cls
        self._set_validator(lambda val: isinstance(val, dict))

    def _apply_new_value(self, value):
        self._value = self._sub_cls(value)
