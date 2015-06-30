class Filter:

    def __init__(self, filter_function, altering_function=None):
        if not filter_function:
            raise TypeError('invalid filter function passed')
        self._filter = filter_function
        self._altering = (altering_function if altering_function else (lambda x: x))

    def __call__(self, *args, **kwargs):
        return self._altering(filter(self._filter, *args))

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
