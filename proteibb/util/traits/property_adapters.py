import re

from proteibb.util.property import Property
from proteibb.util.extension import Extension, ExtensionMixin


class PropertyAdapter(Property):
    """
    General class describing an adapter for a property which can change
    value of the property to have specific behavior.
    """
    class Arguments:

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    def __init__(self, name, default_value, is_optional, cls, cls_args):
        if not issubclass(cls, Property):
            raise TypeError('invalid class type passed as an argument for internal property')
        self._cls = cls
        if not isinstance(cls_args, PropertyAdapter.Arguments):
            raise TypeError('invalid arguments passed as an arguments for internal property')
        self._cls_args = cls_args
        Property.__init__(self, name, default_value, is_optional)
        # Validator should be set by successor.

    def _make(self, value):
        prop = self._cls('temporary', *self._cls_args.args, **self._cls_args.kwargs)
        prop.set_value(value)
        return prop.get_value()


class PropertyListAdapter(PropertyAdapter):
    """
    List adapter changes a property to a list of properties of a current type.
    """
    def __init__(self, name, is_optional, cls, cls_args=PropertyAdapter.Arguments()):
        PropertyAdapter.__init__(self, name, [], is_optional, cls, cls_args)
        self._set_validator(lambda val: isinstance(val, list) and len(val))

    def _apply_new_value(self, values_list):
        self._value = []
        for value in values_list:
            self._value.append(self._make(value))

class ExtensionPropertyListAdapter(PropertyListAdapter, ExtensionMixin):
    """
    List adapter with extensible interface.
    """
    def __init__(self, name, is_optional, cls, cls_args=PropertyAdapter.Arguments()):
        PropertyListAdapter.__init__(self, name, is_optional, cls, cls_args)
        # ExtensionMixin.__init__(self)

    def _container(self):
        return self._value

class ExtensionAdapter(PropertyAdapter):
    """
    Extension adapter which changes a property to have a modification flag.
    """
    def __init__(self, name, is_optional, cls, cls_args=PropertyAdapter.Arguments()):
        PropertyAdapter.__init__(self, name, None, is_optional, cls, cls_args)
        self._set_validator(lambda val: isinstance(val, str) and re.match('^(?:\+|\-)(?!\+|\-).+', val))

    def _apply_new_value(self, value):
        self._value = Extension(value[0], self._make(value[1:]))
