class Filter:

    def __init__(self, filter_function):
        if not filter_function:
            raise TypeError('invalid filter function passed')
        self._filter = filter_function

    def __call__(self, *args, **kwargs):
        return filter(self._filter, *args)

class AlteringFilter(Filter):

    def __init__(self, filter_instance):
        Filter.__init__(self, filter_instance._filter)

    def __call__(self, *args, **kwargs):
        for obj in Filter.__call__(*args, **kwargs):
            self._alter(obj)

    def _alter(self, obj):
        raise NotImplementedError()

def apply_filter_set(*args):
    def processor(objects):
        for a in args:
            if not isinstance(a, Filter):
                raise TypeError('invalid filter set arguments')
            objects = a(objects)
        return objects
    return processor
