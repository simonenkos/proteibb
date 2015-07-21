from proteibb.util.traits.altering_filter import *


class EmptyFiler(Filter):

    def __init__(self):
        Filter.__init__(self, lambda obj: True)

class ClassNameFilter(AlteringFilter):

    def __init__(self, desired_name):
        AlteringFilter.__init__(self, lambda obj: type(obj).__name__.lower() == desired_name,
                                ClassNameFilter._altering_function)

    @staticmethod
    def _altering_function(obj_list):
        if len(obj_list) != 1:
            raise ValueError('unexpected count of objects was filtered by ClassNameFilter')
        return obj_list[0]
