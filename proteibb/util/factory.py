class FactoryInterface:

    class NoFactoryException(Exception):
        pass

    class NoClassRegistered(Exception):
        pass

    def __init__(self):
        self._registry = []

    def register(self, cls):
        self._registry.append(cls)

    def make(self, *args, **kwargs):
        raise NotImplementedError()


class NamedFactory(FactoryInterface):

    def __init__(self, arg_name):
        if not arg_name:
            raise ValueError('empty name for a named factory')
        self._arg_name = arg_name
        FactoryInterface.__init__(self)

    def make(self, *args, **kwargs):
        if self._arg_name not in kwargs:
            raise SyntaxError('invalid arguments passed to named factory')
        for cls in self._registry:
            if cls.__name__.lower() == kwargs[self._arg_name].lower():
                return cls(*args, **kwargs)
        raise FactoryInterface.NoClassRegistered()


class ObjectFactory(FactoryInterface):

    def __init__(self):
        FactoryInterface.__init__(self)

    def make(self, *args, **kwargs):
        if len(self._registry) != 1:
            raise ValueError('invalid usage of object factory')
        cls = self._registry[0]
        return cls(*args, **kwargs)


def register_class(factory):
    def wrapper(cls):
        if not isinstance(factory, FactoryInterface):
            raise FactoryInterface.NoFactoryException()
        factory.register(cls)
        return cls
    return wrapper
