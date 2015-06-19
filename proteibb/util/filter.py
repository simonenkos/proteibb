class Filter:

    def __init__(self, filter_function):
        if not filter_function:
            raise TypeError('invalid filter function passed')
        self._filter = filter_function

    def __call__(self, *args, **kwargs):
        return filter(self._filter, args)

def apply_filter_set(*args):
    def processor(objects):
        fs = []
        for a in args:
            if not isinstance(a, Filter):
                raise TypeError('invalid filter set arguments')
            fs.append(a(objects))
        return fs
    return processor
