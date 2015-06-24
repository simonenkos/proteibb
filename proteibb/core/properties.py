import re
import rfc3987

from proteibb.util import *
from proteibb.util.property import *
from proteibb.core.project.dependency import *

# General properties.

class StringProperty(Property):

    def __init__(self, name, is_optional=False):
        Property.__init__(self, name, "", is_optional)
        self._set_validator(lambda val: isinstance(val, str) and len(val))

    def include_value(self, value):
        self._value = value

class EnumerationProperty(Property):

    def __init__(self, name, enumeration, is_optional=False):
        Property.__init__(self, name, "", is_optional)
        if not isinstance(enumeration, list) or not enumeration:
            raise SyntaxError("invalid enumeration for '" + name + "' property")
        self._set_validator(lambda val: val in enumeration)

# Specialized properties.

class TypeProperty(EnumerationProperty):

    def __init__(self, is_optional=False):
        EnumerationProperty.__init__(self, 'type', ['library', 'application', 'test'], is_optional)

class UrlProperty(Property):

    def __init__(self, is_optional=False):
        Property.__init__(self, 'url', "", is_optional)
        self._set_validator(lambda val: isinstance(val, str) and len(val) and rfc3987.match(val, 'URI') is not None)

class VcsProperty(EnumerationProperty):

    def __init__(self, is_optional=False):
        EnumerationProperty.__init__(self, 'vcs', ['svn', 'git', 'hg'], is_optional)

class VersionProperty(Property):

    def __init__(self, is_optional=False):
        Property.__init__(self, 'version', '', is_optional)
        self._set_validator(lambda val: isinstance(val, str) and len(val) and re.match('^(?:\d+)(?:\.\d+)*$', val))

    def _apply_new_value(self, value):
        self._value = split_version(value)

    def include_value(self, new_value):
        if new_value:
            self._value = new_value

class DependencyProperty(Property):

    def __init__(self, is_optional=False):
        Property.__init__(self, 'dependency', None, is_optional)
        regex_str = '^(?:\w+)(?:(?::(?:=|>|<)\d+)(?:\.\d+)*)*$'
        validator = lambda val: isinstance(val, str) and len(val) and re.match(regex_str, val)
        self._set_validator(validator)

    def _apply_new_value(self, value):
        dep_details = value.split(':')
        self._value = Dependency(dep_details[0])
        for version in dep_details[1:]:
            v = split_version(version[1:])
            q = version[0]
            self._value.add_version(v, q)

class ExtensionProperty(Property):

    def __init__(self, name, extension_property_handler_cls, is_optional=True):
        Property.__init__(self, name, None, is_optional)
        self._extension_property_handler_cls = extension_property_handler_cls
        self._set_validator(lambda val: isinstance(val, dict))

    def _apply_new_value(self, value):
        self._value = self._extension_property_handler_cls(value)
