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
        if not self._property_validator(val):
            raise SyntaxError("invalid value for '" + self._name + "' property")
        self._apply_new_value(val)

    def _set_validator(self, validator):
        self._property_validator = validator

    def _apply_new_value(self, value):
        self._value = value
