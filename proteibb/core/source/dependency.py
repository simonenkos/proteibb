class Dependency:

    def __init__(self, name):
        self._name = name
        self._exact = []
        self._min = None
        self._max = None

    def add_version(self, version, qualification):
        if qualification is '':
            self._add_exact_version(version)
        elif qualification is '>':
            self._add_min(version)
        elif qualification is '<':
            self._add_max(version)
        else:
            raise SyntaxError("invalid version (" + version
                              + ") qualification '" + qualification
                              + "' for dependency: " + self._name)

    def _add_exact_version(self, version):
        if self._min and version < self._min:
            raise SyntaxError("dependency '" + self._name +
                              "' version conflict: " + version +
                              " and min " + self._min)
        if self._max and version > self._max:
            raise SyntaxError("dependency '" + self._name +
                              "' version conflict: " + version +
                              " and max " + self._max)
        if version not in self._exact:
            self._exact.append(version)

    def _add_min(self, version):
        if not self._min or version > self._min:
            if self._max and version >= self._max:
                raise SyntaxError("dependency '" + self._name +
                                  "' version conflict: min " + version +
                                  " and max " + self._max)
            self._exact = [v for v in self._exact if v >= version]
            self._min = version

    def _add_max(self, version):
        if not self._max or version < self._max:
            if self._min and version <= self._min:
                raise SyntaxError("dependency '" + self._name +
                                  "' version conflict: max " + version +
                                  " and min " + self._min)
            self._exact = [v for v in self._exact if v <= version]
            self._max = version
