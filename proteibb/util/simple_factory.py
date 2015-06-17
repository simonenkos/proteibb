class NoFactoryException(Exception):
    pass

# Simple class factory.

class SimpleFactory:

    def __init__(self):
        self._registry = []

    def register(self, cls):
        self._registry.append(cls)

    def make(self, *args, **kwargs):
        objects = []
        for cls in self._registry:
            obj = cls(*args, **kwargs)
            objects.append(obj)
        return objects

def register_at_factory(factory):
    def wrapper(cls):
        if not isinstance(factory, SimpleFactory):
            raise NoFactoryException()
        factory.register(cls)
        return cls
    return wrapper
