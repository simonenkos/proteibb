class Property:

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
                raise SyntaxError("invalid value for '" + self._name + "' property")
            self._apply_new_value(val)

    def _set_validator(self, validator):
        self._property_validator = validator

    def _apply_new_value(self, value):
        self._value = value


class StringProperty(Property):

    def __init__(self, name, is_optional=False):
        Property.__init__(self, name, "", is_optional)
        self._set_validator(lambda val: isinstance(val, str))


class StringsListProperty(Property):

    def __init__(self, name, is_optional=False):
        Property.__init__(self, name, [], is_optional)

        def validate(val):
            if not isinstance(val, list):
                return False
            for p in val:
                if not isinstance(p, str) or not len(p):
                    return False
            return True
        self._set_validator(validate)


class EnumerationProperty(Property):

    def __init__(self, name, enumeration, is_optional=False):
        Property.__init__(self, name, "", is_optional)
        if not isinstance(enumeration, list) or not enumeration:
            raise SyntaxError("invalid enumeration for '" + name + "' property")
        self._set_validator(lambda val: val in enumeration)
