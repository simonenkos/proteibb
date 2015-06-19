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

    @staticmethod
    def is_same_property(fst, snd):
        if not isinstance(fst, Property) or not isinstance(snd, Property) or type(snd) != type(fst):
            return False
        if fst.get_name() != snd.get_name():
            return False
        return True

    def include_value(self, value):
        raise ValueError("appending of values is not supported for a current property type")

    def exclude_value(self, value):
        raise ValueError("removing of values is not supported for a current property type")

# Property changing policies.

def include_property_value(dst_prop, src_prop):
    if not Property.is_same_property(dst_prop, src_prop):
        raise TypeError('cannot append a new value to a property: type conflict')
    dst_prop.append_value(src_prop)

def exclude_property_value(dst_prop, src_prop):
    if not Property.is_same_property(dst_prop, src_prop):
        raise TypeError('cannot remove a value from a property: type conflict')
    dst_prop.remove_value(src_prop)

# Additional specialized properties.

class StringProperty(Property):

    def __init__(self, name, is_optional=False):
        Property.__init__(self, name, "", is_optional)
        self._set_validator(lambda val: isinstance(val, str))

    def include_value(self, value):
        self._value = value

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

    def include_value(self, strings_list):
        for string in strings_list:
            if string not in self._value:
                self._value.append(string)

    def exclude_value(self, strings_list):
        for string in strings_list:
            if string in self._value:
                self._value.remove(string)

class EnumerationProperty(Property):

    def __init__(self, name, enumeration, is_optional=False):
        Property.__init__(self, name, "", is_optional)
        if not isinstance(enumeration, list) or not enumeration:
            raise SyntaxError("invalid enumeration for '" + name + "' property")
        self._set_validator(lambda val: val in enumeration)
