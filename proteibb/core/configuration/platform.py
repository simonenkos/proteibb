class Platform:

    def __init__(self, name, options):
        self._name = name
        self._options = options

    def get_name(self):
        return self._name

    def get_options(self):
        return self._options
