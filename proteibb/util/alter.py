class Alter:
    """
    Utility object that allows to change other object with altering function.
    """
    def __init__(self, altering_function):
        if not altering_function:
            altering_function = (lambda x: x)
        self._altering_function = altering_function

    def __call__(self, *args, **kwargs):
        return self._altering_function(*args, **kwargs)
