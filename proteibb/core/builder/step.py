class Step:
    """
    Interface for step representation at build system.
    """
    def __init__(self, data_callback, step_callback):
        if not data_callback:
            raise ValueError('invalid data callback passed to a step')
        if not step_callback:
            raise ValueError('invalid step callback passed to a step')
        self._data_callback = data_callback
        self._step_callback = step_callback

    def data(self):
        return self._data_callback()

    def step(self):
        return self._step_callback()
