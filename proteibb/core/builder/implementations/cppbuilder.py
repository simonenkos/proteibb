from proteibb.core.builder import builder
from proteibb.core.options import OptionBase
from proteibb.core.platforms import PlatformBase
from proteibb.core.properties import *

from buildbot.plugins import util

from proteibb.core.builder.steps.checkout import Checkout
from proteibb.core.builder.steps.compile import Compile


class CppBuilder(builder.Builder):

    options_factory = ObjectFactory()
    platforms_factory = ObjectFactory()

    def __init__(self, data):
        builder.Builder.__init__(self, data, CppBuilder.options_factory, CppBuilder.platforms_factory)

    def make(self, configuration, project):
        builders = []
        for branch in project.branches():
            # ToDo: Steps to add:
            # - Checkout step (not depends on the builder type [nd])
            # - Find all sources and process them according to valid file extension list and excludes (need to modify
            # project structure) [nd].
            # - For each source call compiler with project specific options (depends on type of the builder [d]).
            # - According to a project type call linker to make app or lib [d]
            for platform in branch.platforms(project):
                chain = [
                    Checkout(project.vcs(), project.code(), project.url(), branch.name(), platform),
                    # Todo: Add next steps.
                ]
                build_factory = util.BuildFactory()
                previous_step_data = None
                for element in chain:
                    element.setup(previous_step_data)
                    previous_step_data = element.data()
                # ToDo: Figure out which parameter need to be used.
                builders.append(util.BuilderConfig(name='???', slavenames=[], factory=build_factory))
        return builders


@register_class(CppBuilder.options_factory)
class Option(OptionBase):

    def __init__(self, data):
        properties = [
            PropertyListAdapter('defines', True, StringProperty),
            PropertyListAdapter('external-libs', True, StringProperty)
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
