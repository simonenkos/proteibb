class Dependency:

    def __init__(self, name):
        self._name = name
        self._versions = []

    def add_version(self, version):
        if version and version not in self._versions:
            self._versions.append(version)

    def get_name(self):
        return self._name

    def get_versions(self):
        return self._versions

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def include(self, other):
        if not isinstance(other, Dependency):
            raise TypeError("invalid type of dependency")
        for version in other.get_versions():
            if version not in self._versions:
                self._versions.append(version)

    def exclude(self, other):
        if not isinstance(other, Dependency):
            raise TypeError("invalid type of dependency")
        if not other.get_versions():
            # If we exclude whole dependency, we need empty
            self._versions = []
        for version in other.get_versions():
            if version in self._versions:
                self._versions.remove(version)
        return not self._versions
