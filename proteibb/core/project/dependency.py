class Dependency:

    def __init__(self, name):
        self._name = name
        self._exact = []
        self._min = None
        self._max = None

    def add_version(self, version, qualification):
        if version:
            if qualification is '=':
                if version not in self._exact:
                    self._exact.append(version)
            elif qualification is '>':
                if self._max and self._max < version:
                    raise SyntaxError("version conflict: 'max' is smaller than 'min'")
                self._min = version
            elif qualification is '<':
                if self._min and self._min > version:
                    raise SyntaxError("version conflict: 'min' is bigger than 'max'")
                self._max = version
            else:
                raise SyntaxError("invalid version (" + str(version)
                                  + ") qualification '" + qualification
                                  + "' for dependency: " + self._name)

    def get_name(self):
        return self._name

    def get_versions(self):
        return {'ver': self._exact,
                'min': self._min,
                'max': self._max}

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    # ToDo think about dependencies

    # def add(self, other):
    #     if not isinstance(other, Dependency):
    #         raise TypeError("invalid type of dependency")
    #     for v in other._exact:
    #         if v not in self._exact:
    #             self._exact.append(v)
    #     self._max = other._max
    #     self._min = other._min
    #
    # def subtract(self, other):
    #     if not isinstance(other, Dependency):
    #         raise TypeError("invalid type of dependency")
    #     for v in other._exact:
    #         if v in self._exact:
    #             self._exact.remove(v)
    #     if self._min == other._min:
    #         self._min = None
    #     if self._max == other._max:
    #         self._max = None
    #     return not self._exact and not self._min and self._max
