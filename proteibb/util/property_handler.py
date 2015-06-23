from copy import deepcopy
from property import Property

class PropertyLookupError(Exception):
    pass

class PropertyHandler:

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

    def apply_change_policy(self, properties_map, change_policy):
        for dst_prop_name, dst_prop in properties_map.items():
            src_prop = self._properties.get(dst_prop_name, None)
            if src_prop:
                change_policy(dst_prop, src_prop)

    @staticmethod
    def replace(func):
        def get_property_value(self):
            prop_name = func.__name__
            if prop_name not in self._properties:
                raise PropertyLookupError(prop_name)
            return self._properties[prop_name].get_value()
        return get_property_value
