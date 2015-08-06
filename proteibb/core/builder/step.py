class Step:
    """
    Interface for step representation at build system.
    """
    def get_step(self, *args, **kwargs):
        raise NotImplementedError()