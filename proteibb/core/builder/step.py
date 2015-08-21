class Step:
    """
    Interface for step representation at build system.
    """
    def setup(self, *args, **kwargs):
        raise NotImplementedError()

    def data(self):
        raise NotImplementedError()

    def step(self):
        raise NotImplementedError()
