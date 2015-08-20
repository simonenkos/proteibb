from copy import deepcopy

from proteibb.core.properties import *


class Branch(Property.Handler):

    def __init__(self, data):
        pparams = PropertyAdapter.Arguments(False, StringProperty)
        oparams = PropertyAdapter.Arguments(False, StringProperty)
        dparams = PropertyAdapter.Arguments(False, StringProperty)
        properties = [
            StringProperty('name'),
            VersionProperty(True),
            PropertyListAdapter('platforms', True, ExtensionAdapter, pparams),
            PropertyListAdapter('options', True, ExtensionAdapter, oparams),
            PropertyListAdapter('dependencies', True, ExtensionAdapter, dparams),
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def version(self):
        pass

    def platforms(self, project):
        return self._get_extension_properties(project, 'platforms')

    def dependencies(self, project):
        return self._get_extension_properties(project, 'dependencies')

    def options(self, project):
        return self._get_extension_properties(project, 'options')

    def _get_extension_properties(self, project, name):
        project_properties = deepcopy(self.properties(project).get(name))
        for prop in self._properties[name].get_value():
            prop.apply(project_properties)
        return project_properties.get_value()
