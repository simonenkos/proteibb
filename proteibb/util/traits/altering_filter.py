from proteibb.util.alter import Alter
from proteibb.util.filter import Filter


class AlteringFilter(Filter, Alter):
    """
    Filter object which change all filtered element with altering function.
    """
    def __init__(self, filtering_function, altering_function=None):
        Filter.__init__(self, filtering_function)
        Alter.__init__(self, altering_function)

    def __call__(self, *args, **kwargs):
        return [Alter.__call__(self, x) for x in Filter.__call__(self, *args, **kwargs)]
