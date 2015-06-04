from source import *

class _SourceFactory:

    def __init__(self):
        self._registry = {}

    def register(self, name, func):
        self._registry[name] = func
        return func

    def make(self, data):
        name = data['name']
        vsc  = data['vcs']
        sources = []
        for name, func in self._registry:
            details = data[name]
            if details:
                sources.append(func(details))
        return sources

source_factory = _SourceFactory()

def add_source_factory(name):
    def factory(function):
        source_factory.register(name, function)
        return function
    return factory
