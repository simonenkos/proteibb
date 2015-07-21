from proteibb.core.builder import builder
from proteibb.core.options import OptionBase
from proteibb.core.platforms import PlatformBase
from proteibb.core.properties import *

from buildbot.plugins import util


class CppBuilder(builder.Builder):

    options_factory = ObjectFactory()
    platforms_factory = ObjectFactory()

    def __init__(self, data):
        builder.Builder.__init__(self, data, CppBuilder.options_factory, CppBuilder.platforms_factory)

    def make(self, configuration, project):
        pt = project.type()
        factory_maker = getattr(self, '_make_' + pt + '_build_factory')
        factory = factory_maker(configuration, project)
        return util.BuilderConfiguration(name=project.name(), slavenames=[], factory=factory)

    def _make_library_build_factory(self, configuration, project):
        factory = util.BuildFactory()
        # factory.addStep() # ToDo
        return factory

    def _make_application_build_factory(self, configuration, project):
        pass


@register_class(CppBuilder.options_factory)
class Option(OptionBase):

    def __init__(self, data):
        properties = [
            PropertyListAdapter('defines', True, StringProperty),
            PropertyListAdapter('external-libs', True, DependencyProperty)
        ]
        OptionBase.__init__(self, data, properties)


@register_class(CppBuilder.platforms_factory)
class Platform(PlatformBase):

    def __init__(self, data):
        properties = [
            StringProperty('cpp-compiler'),
            StringProperty('c-compiler'),
            StringProperty('archiver'),
            StringProperty('strip'),
            PathProperty('bin-path', True),
            PathProperty('lib-path', True),
            PathProperty('sys-root', True),
        ]
        PlatformBase.__init__(self, data, properties)
