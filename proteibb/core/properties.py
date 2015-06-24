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


# class SingleVersionProperty(VersionProperty):
#
#     def __init__(self, is_optional=True):
#         VersionProperty.__init__(self, 'version', '', is_optional)
#         self._set_validator(VersionProperty.validator)
#
# class MultipleVersionProperty(VersionProperty):
#
#     def __init__(self, is_optional=True):
#         VersionProperty.__init__(self, 'versions', [], is_optional)
#
#         def validate(val):
#             if not isinstance(val, list):
#                 return False
#             for version in val:
#                 if not VersionProperty.validator(version):
#                     return False
#             return True
#         self._set_validator(validate)
#
#     def _apply_new_value(self, value):
#         version = []
#         for v in value:
#             version.append(split_version(v))
#         Property._apply_new_value(self, version)

# # Dependency property variations.
#
# class DependenciesProperty(Property):
#     def __init__(self, is_optional=True):
#         Property.__init__(self, 'dependencies', [], is_optional)
#
#         def validate(val):
#             if not isinstance(val, list):
#                 return False
#             for dep in val:
#                 if not isinstance(dep, str) or not re.match('^(?:\w+)(?:(?::(?:=|>|<)\d+)(?:\.\d+)*)*$', dep):
#                     return False
#             return True
#         self._set_validator(validate)
#
#     def _apply_new_value(self, dep_list):
#         dependencies = []
#         for dep in dep_list:
#             dep_details = dep.split(':')
#             d = Dependency(dep_details[0])
#             for version in dep_details[1:]:
#                 v = split_version(version[1:])
#                 q = version[0]
#                 d.add_version(v, q)
#             dependencies.append(d)
#         Property._apply_new_value(self, dependencies)
#
#     def include_value(self, dependency_list):
#         if dependency_list:
#             for incoming_dep in dependency_list:
#                 for dep in self._value:
#                     if incoming_dep.get_name() == dep.get_name():
#                         dep.add(incoming_dep)
#                         return
#                 self._value.append(incoming_dep)
#
#     def exclude_value(self, dependency_list):
#         if dependency_list:
#             for incoming_dep in dependency_list:
#                 for dep in self._value:
#                     if incoming_dep.get_name() == dep.get_name():
#                         if dep.subtract(incoming_dep):
#                             self._value.remove(dep)

class ExtensionProperty(Property):

    def __init__(self, name, extension_property_handler_cls, is_optional=True):
        Property.__init__(self, name, None, is_optional)
        self._extension_property_handler_cls = extension_property_handler_cls
        self._set_validator(lambda val: isinstance(val, dict))

    def _apply_new_value(self, value):
        self._value = self._extension_property_handler_cls(value)
