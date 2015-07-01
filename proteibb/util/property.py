import re

from copy import deepcopy

class Property:
    """
    Class represents an attribute of some configuration which
    have a name and a value that need to be set up and checked
    for correctness.
    """
    def __init__(self, name, default_value=None, is_optional=False):
        self._name = name
        self._value = default_value
        self._is_optional = is_optional
        self._property_validator = None

    def get_name(self):
        return self._name

    def is_optional(self):
        return self._is_optional

    def get_value(self):
        return self._value

    def set_value(self, val):
        if not self._property_validator:
            raise NotImplementedError()
        if not self._is_optional and not val:
            raise SyntaxError("no required property with name '" + self._name + "' was found")
        if val is not None:
            if not self._property_validator(val):
                raise SyntaxError("an invalid value for '" + self._name + "' property")
            self._apply_new_value(val)

    def _set_validator(self, validator):
        self._property_validator = validator

    def _apply_new_value(self, value):
        self._value = value

    # class NoExpandException(Exception):
    #     pass
    #
    # @staticmethod
    # def is_available_for_extend(dst, src, method):
    #     if not isinstance(dst, Property) or not isinstance(src, Property) or type(dst) != type(src):
    #         return False
    #     if dst.get_name() != src.get_name():
    #         return False
    #     # Check methods was implemented.
    #     try:
    #         method(None)
    #         return True
    #     except Property.NoExpandException:
    #         return False
    #     except:
    #         return True
    #
    # def include_value(self, value):
    #     raise Property.NoExpandException
    #
    # def exclude_value(self, value):
    #     raise Property.NoExpandException
    #
    # # A property changing policies.
    #
    # @staticmethod
    # def include(dst_prop, src_prop):
    #     if not Property.is_available_for_extend(dst_prop, src_prop, dst_prop.include_value):
    #         raise TypeError('cannot append a new value to a property: not available for extend')
    #     dst_prop.include_value(src_prop.get_value())
    #
    # @staticmethod
    # def exclude(dst_prop, src_prop):
    #     if not Property.is_available_for_extend(dst_prop, src_prop,  dst_prop.exclude_value):
    #         raise TypeError('cannot remove a value from a property: not available for extend')
    #     dst_prop.exclude_value(src_prop.get_value())

    # A handler that helps to manipulate with properties.

    class LookupError(Exception):
        pass

    class Handler:

        def __init__(self, properties, data):
            self._properties = {}
            if data is None:
                raise SyntaxError("empty property set")
            for prop in properties:
                prop_name = prop.get_name()
                if not isinstance(prop, Property):
                    raise SyntaxError('an invalid property class was provided for creation')
                self._properties[prop_name] = deepcopy(prop)
                self._properties[prop_name].set_value(data.get(prop_name, None))

        @staticmethod
        def replace(func):
            def get_property_value(self):
                prop_name = func.__name__
                if prop_name not in self._properties:
                    raise Property.LookupError(prop_name)
                return self._properties[prop_name].get_value()
            return get_property_value

# List adapter changes a property to a list of properties of a current type.

class PropertyListAdapter(Property):

    def __init__(self, name, is_optional, list_cls, *args, **kwargs):
        self._list_cls = list_cls
        self._list_cls_args = args
        self._list_cls_kwargs = kwargs
        Property.__init__(self, name, [], is_optional)
        self._set_validator(lambda val: isinstance(val, list) and len(val))

    def _apply_new_value(self, values_list):
        self._value = []
        for value in values_list:
            prop = self._list_cls('temporary', *self._list_cls_args, **self._list_cls_kwargs)
            prop.set_value(value)
            self._value.append(prop.get_value())

# Extension adapter which changes a property to have a modification flag.

class ExtensionAdapter(Property):

    def __init__(self, name, is_optional, extension_cls, *args, **kwargs):
        self._extension_cls = extension_cls
        self._extension_cls_args = args
        self._extension_cls_kwargs = kwargs
        Property.__init__(self, name, None, is_optional)
        self._set_validator(lambda val: isinstance(val, str) and re.match('^(?:\+|\-)(?!\+|\-).+', val))

    def _apply_new_value(self, value):
        modification = value[0]
        prop = self._extension_cls('temporary', *self._extension_cls_args, **self._extension_cls_kwargs)
        prop.set_value(value[1:])
        self._value = {'ext': modification, 'val': prop.get_value()}

    # @staticmethod
    # def _check_extensions(val):
    #     if not isinstance(val, list) or not len(val):
    #         return False
    #     for ext in val:
    #         if not isinstance(ext, str) or not re.match('^(?:\+|\-)(?!\+|\-).+', ext):
    #             return False
    #     return True
    #
    # def _apply_new_value(self, values_list):
    #     self._value = []
    #     for value in values_list:
    #         prop = self._property_cls('temporary', self._property_cls_args, self._property_cls_kwargs)
    #         prop.set_value(value)
    #         self._value.append(prop.get_value())
    #
    # def extend(self, values_list):
    #     for new_val in values_list:
    #         new_val_not_in_list = True
    #         for val in self._value:
    #             if new_val == val:
    #                 new_val_not_in_list = False
    #                 if hasattr(val, 'include'):
    #                     val.include(new_val)
    #         if new_val_not_in_list:
    #             self._value.append(new_val)
    #
    # def exclude(self, values_list):
    #     for new_val in values_list:
    #         need_to_remove = True
    #         for val in self._value:
    #             if new_val == val and hasattr(val, 'exclude'):
    #                 need_to_remove = val.exclude(new_val)
    #         if need_to_remove:
    #             self._value.remove(new_val)
