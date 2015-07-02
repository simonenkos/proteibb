import re

from proteibb.util.property import Property
from proteibb.util.extensible_mixin import ExtensibleMixin


class PropertyAdapter(Property):
    """

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

    def _make(self):
        return self._cls('temporary', *self._cls_args.args, **self._cls_args.kwargs)


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
            prop = self._make()
            prop.set_value(value)
            self._value.append(prop.get_value())


class ExtensionPropertyListAdapter(PropertyListAdapter, ExtensibleMixin):
    """
    List adapter with extensible interface.
    """
    def __init__(self, name, is_optional, cls, cls_args=PropertyAdapter.Arguments()):
        PropertyListAdapter.__init__(self, name, is_optional, cls, cls_args)
        ExtensibleMixin.__init__(self, self._value)

class ExtensionAdapter(PropertyAdapter):
    """
    Extension adapter which changes a property to have a modification flag.
    """
    def __init__(self, name, is_optional, cls, cls_args=PropertyAdapter.Arguments()):
        PropertyAdapter.__init__(self, name, None, is_optional, cls, cls_args)
        self._set_validator(lambda val: isinstance(val, str) and re.match('^(?:\+|\-)(?!\+|\-).+', val))

    def _apply_new_value(self, value):
        modification = value[0]
        prop = self._make()
        prop.set_value(value[1:])
        self._value = {'mod': modification, 'val': prop.get_value()}

    def apply(self, property_list):
        if not isinstance(property_list, ExtensionPropertyListAdapter):
            raise TypeError('unknown type of property list')
        ext_mod = self.get_value()['mod']
        ext_val = self.get_value()['val']
        if ext_mod == '+':
            property_list.include(ext_val)
        else:
            property_list.exclude(ext_val)
