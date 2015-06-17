from proteibb.util.property import Property, StringProperty
from dependency import Dependency

import rfc3987
import re

# Common properties and mixins.

class DetailedPropertyMixin:

    def __init__(self, is_detail_specific):
        self._is_detail_specific = is_detail_specific

    def is_detail_specific(self):
        return self._is_detail_specific

class DetailedStringProperty(StringProperty, DetailedPropertyMixin):

    def __init__(self, name, is_optional=True, is_detail_specific=True):
        StringProperty.__init__(self, name, is_optional)
        DetailedPropertyMixin.__init__(self, is_detail_specific)


# Source properties specializations.

class UrlProperty(Property, DetailedPropertyMixin):

    def __init__(self):
        Property.__init__(self, 'url', "")
        DetailedPropertyMixin.__init__(self, False)
        self._set_validator(lambda val: isinstance(val, str) and len(val) and rfc3987.match(val, 'URI') is not None)

class VcsProperty(Property, DetailedPropertyMixin):

    def __init__(self):
        Property.__init__(self, 'vcs', "")
        DetailedPropertyMixin.__init__(self, False)
        self._set_validator(lambda val: isinstance(val, str) and len(val) and val in ['svn', 'git', 'hg'])

class VersionsProperty(Property, DetailedPropertyMixin):

    def __init__(self):
        Property.__init__(self, 'versions', [], True)
        DetailedPropertyMixin.__init__(self, True)

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

class DependenciesProperty(Property, DetailedPropertyMixin):

    def __init__(self):
        Property.__init__(self, 'dependencies', [], True)
        DetailedPropertyMixin.__init__(self, True)

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
