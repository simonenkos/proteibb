class Filter:
    """
    Utility class that helps with using filters on sets.
    """
    def __init__(self, filter_function):
        if not filter_function:
            raise TypeError('invalid filter function was passed')
        self._filter = filter_function

    def __call__(self, *args, **kwargs):
        return filter(self._filter, *args)

def apply_filter_set_serial(*args):
    def processor(objects):
        for a in args:
            if not isinstance(a, Filter):
                raise TypeError('invalid filter set arguments')
            objects = a(objects)
        return objects
    return processor

def apply_filter_set_parallel(*args):
    def processor(objects):
        new_objects = []
        for a in args:
            if not isinstance(a, Filter):
                raise TypeError('invalid filter set arguments')
            new_objects.extend(a(objects))
        return new_objects
    return processor
