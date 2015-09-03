from proteibb.util.alter import Alter
from proteibb.util.filter import Filter

from itertools import chain


class AlteringFilter(Filter, Alter):
    """
    Filter object which change all filtered element with altering function.
    """
    def __init__(self, filtering_function, altering_function=None, individual_altering=True):
        Filter.__init__(self, filtering_function)
        Alter.__init__(self, altering_function)
        self._individual_altering = individual_altering

    def __call__(self, *args, **kwargs):
        filtered = Filter.__call__(self, *args, **kwargs)
        if self._individual_altering:
            return [Alter.__call__(self, x) for x in filtered]
        else:
            return Alter.__call__(self, filtered)

