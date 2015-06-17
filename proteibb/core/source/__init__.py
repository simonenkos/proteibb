from proteibb.util.simple_factory import SimpleFactory

class SourceFactory(SimpleFactory):

    def __init__(self):
        SimpleFactory.__init__(self)

    def make(self, data):
        sources = []
        for cls in self._registry:
            details_name = cls.__name__.lower()
            details_list = data.get(details_name, None)
            if details_list is None:
                raise SyntaxError("no '" + details_name + "' section in configuration")
            for details in details_list:
                sources.append(cls(data, details))
        return sources

# Create sources factory instance.
source_factory = SourceFactory()
