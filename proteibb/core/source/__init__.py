from source import *
from properties import *
from dependency import *

class _SourceFactory:

    def __init__(self):
        self._registry = []

    def register(self, func):
        self._registry.append(func)

    def make(self, data):
        sources = []
        for func in self._registry:
            sources.append(func(data))
        return sources

source_factory = _SourceFactory()

def add_source_factory(function):
    source_factory.register(function)
    return function
