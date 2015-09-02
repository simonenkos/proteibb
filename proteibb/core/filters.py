from proteibb.util.traits.altering_filter import *


class EmptyFiler(Filter):

    def __init__(self):
        Filter.__init__(self, lambda obj: True)


class ClassNameFilter(AlteringFilter):

    def __init__(self, desired_name):
        AlteringFilter.__init__(self, lambda obj: type(obj).__name__.lower() == desired_name)

    def __call__(self, *args, **kwargs):
        object_list = AlteringFilter.__call__(self, *args, **kwargs)
        if len(object_list) != 1:
            raise ValueError('unexpected count of objects was filtered by ClassNameFilter')
        return object_list[0]
