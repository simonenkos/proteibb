from copy import deepcopy
from property import Property

class PropertyHandler:

    __dpl = {}

    def __init__(self):
        self._properties = {}
        for prop_name, prop in self.__dpl.items():
            self._properties[prop_name] = deepcopy(prop)

    @staticmethod
    def declare_property(property_class, name_setup_requested=False, **kwargs):
        def wrapper(func):
            if not issubclass(property_class, Property):
                raise SyntaxError('an invalid property class was provided for creation')
            prop_name = func.__name__
            if name_setup_requested:
                kwargs['name'] = prop_name
            if prop_name in PropertyHandler.__dpl:
                raise SyntaxError('redefinition of a property: ' + prop_name)
            prop = property_class(**kwargs)
            if prop_name != prop.get_name():
                raise SyntaxError("property name conflict: method name is '" + prop_name +
                                  "'; property name is '" + prop.get_name() + "'")
            PropertyHandler.__dpl[prop_name] = prop
            return lambda self: self._properties[prop_name]
        return wrapper
