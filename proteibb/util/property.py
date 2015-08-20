from copy import deepcopy


class Property:
    """
    Class represents an attribute of some configuration which
    have a name and a value that need to be set up and checked
    for correctness.
    """
    def __init__(self, name, default_value=None, is_optional=False, *args, **kwargs):
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

        @staticmethod
        def properties(handler):
            if not isinstance(handler, Property.Handler):
                raise TypeError('invalid type of a property handler')
            return handler._properties
