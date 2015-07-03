from proteibb.util.extension import ExtensionMixin

class Dependency(ExtensionMixin):
    """
    Current class describes objects which represent a dependency for a some project with set of versions.
    To make the class to be available for extension, we need to redefine include/exclude methods
    to manipulate with versions correctly, because a value for extension is not a single version,
    but a list of versions.
    """
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

    def _container(self):
        # Return raw list of version to move on a next layer of extension procedure.
        return self._versions

    def include(self, value):
        for v in value:
            # Iterate over versions list.
            ExtensionMixin.include(self, v)

    def exclude(self, value):
        if not value:
            # If only name was provided we need to remove current dependency.
            return True
        for v in value:
            # Iterate over versions list.
            ExtensionMixin.exclude(self, v)
        return not self._versions

    def __eq__(self, other):
        if not isinstance(other, Dependency):
            raise TypeError('invalid type of object')
        return self.get_name() == other.get_name()

    def _strip(self, value):
        if not isinstance(value, Dependency):
            raise TypeError('invalid type of object used for strip')
        # Get a list of versions from external dependency.
        return value.get_versions()
