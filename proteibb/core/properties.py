import rfc3987
import inspect
import os

from proteibb.util import *
from proteibb.util.traits import *
from proteibb.util.factory import *

# General properties.


class StringProperty(Property):

    def __init__(self, name, is_optional=False, *args, **kwargs):
        Property.__init__(self, name, "", is_optional, *args, **kwargs)
        self._set_validator(lambda val: (isinstance(val, str) or isinstance(val, unicode)) and (len(val) > 0))


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
        self._set_validator(lambda val: (isinstance(val, str) or isinstance(val, unicode)) and (len(val) > 0) and
                                        rfc3987.match(val, 'URI') is not None)


class VcsProperty(EnumerationProperty):

    def __init__(self, is_optional=False, *args, **kwargs):
        EnumerationProperty.__init__(self, 'vcs', ['svn', 'git', 'hg'], is_optional, *args, **kwargs)


class VersionProperty(Property):

    def __init__(self, is_optional=False, *args, **kwargs):
        Property.__init__(self, 'version', '', is_optional, *args, **kwargs)
        self._set_validator(lambda val: (isinstance(val, str) or isinstance(val, unicode)) and
                                        (len(val) > 0) and re.match('^(?:\d+)(?:\.\d+)*$', val))

    def _apply_new_value(self, value):
        self._value = split_version(value)


class SubProperty(Property):

    def __init__(self, name, is_optional, cls, *args, **kwargs):
        if not issubclass(cls, Property.Handler):
            raise TypeError('invalid sub property class type')
        Property.__init__(self, name, None, is_optional, *args, **kwargs)
        self._sub_cls = cls
        self._set_validator(lambda val: isinstance(val, dict))

    def _apply_new_value(self, value):
        self._value = self._sub_cls(value)


class GroupProperty(Property):

    def __init__(self, name, is_optional, group_cls, factory, *args, **kwargs):
        if not isinstance(factory, FactoryInterface):
            raise TypeError('invalid factory type')
        if not inspect.isclass(group_cls):
            raise TypeError('invalid group type')
        Property.__init__(self, name, {}, is_optional, *args, **kwargs)
        self._set_validator(lambda val: isinstance(val, dict) and (len(val) > 0))
        self._factory = factory
        self._group_cls = group_cls

    def _apply_new_value(self, value):
        self._value = self._group_cls(value, self._factory)


class PathProperty(Property):

    def __init__(self, name, is_optional=False, *args, **kwargs):
        Property.__init__(self, name, "", is_optional, *args, **kwargs)
        self._set_validator(lambda val: (isinstance(val, str) or isinstance(val, unicode)) and
                                        (len(val) > 0) and os.path.exists(val))
