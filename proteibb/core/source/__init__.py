class _SourceFactory:

    def __init__(self):
        self._registry = []

    def register(self, cls):
        self._registry.append(cls)

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

source_factory = _SourceFactory()

def add_source_factory(cls):
    source_factory.register(cls)
    return cls
