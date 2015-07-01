from proteibb.util.simple_factory import *

class ConfigurationFactory(SimpleFactory):

    def __init__(self):
        SimpleFactory.__init__(self)

    def make(self, *args, **kwargs):
        if not kwargs.has_key('conf_name'):
            raise SyntaxError('invalid arguments passed to configuration factory')
        for cls in self._registry:
            if cls.__name__.lower() == kwargs['conf_name'].lower():
                return cls(*args, **kwargs)
        raise TypeError('factory error: no configuration class found')

conf_factory = ConfigurationFactory()
