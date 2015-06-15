from copy import deepcopy
from property import Property

class PropertyHandler:

    __dpl = {}

    def __init__(self):
        self._properties = {}
        for prop_name, prop in self.__dpl.items():
            self._properties[prop_name] = deepcopy(prop)

    @staticmethod
    def declare_property(property_class, **kwargs):
        def wrapper(func):
            if not issubclass(property_class, Property):
                raise SyntaxError('an invalid property class was provided for creation')
            prop_name = func.__name__
            kwargs['name'] = prop_name
            if prop_name in PropertyHandler.__dpl:
                raise SyntaxError('redefinition of a property: ' + prop_name)
            PropertyHandler.__dpl[prop_name] = property_class(**kwargs)
            return lambda self: self._properties[prop_name]
        return wrapper
