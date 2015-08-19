class Step:
    """
    Interface for step representation at build system.
    """
    def __init__(self, data_callback, step_callback):
        self._data_callback = data_callback
        self._step_callback = step_callback

    def data(self):
        if not self._data_callback:
            raise ValueError('invalid data callback passed to a step')
        return self._data_callback()

    def step(self):
        if not self._step_callback:
            raise ValueError('invalid step callback passed to a step')
        return self._step_callback()
