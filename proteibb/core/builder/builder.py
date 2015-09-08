from proteibb.core.properties import *
from proteibb.core.options import OptionsGroup
from proteibb.core.platforms import PlatformsGroup
from proteibb.core.builder.steps.checkout import Checkout
from proteibb.core.vcs.vcs import VCS

from buildbot.plugins import util


class Builder(Property.Handler):
    """
    Example of builder json configuration file:
    {
        "name" : "builder-name",
        "slaves" : [
            "slave_x86_release",
            "slave_x86_debug"
        ],
        "options" : { ... },
        "platforms" : { ... },
    }
    This class describes a base structure of a builder. Successors of this class should
    implement specific properties of a concrete builder in addition to existing ones.
    """
    def __init__(self, data, options_factory, platforms_factory):
        properties = [
            StringProperty('name'),
            GroupProperty('options', False, OptionsGroup, options_factory),
            GroupProperty('platforms', True, PlatformsGroup, platforms_factory)
        ]
        Property.Handler.__init__(self, properties, data)

    @Property.Handler.replace
    def name(self):
        pass

    @Property.Handler.replace
    def options(self):
        pass

    @Property.Handler.replace
    def platforms(self):
        pass

    def make(self, configuration, project):
        builders = []
        # Iterate over all branches of a project.
        for branch in project.branches():
            project_vcs = project.vcs()
            project_code = project.code()
            branch_name = branch.name()
            # Make builders for each platform configured at the project specification.
            for platform_name in branch.platforms(project):
                try:
                    # Check for a platform configuration at the builder.
                    platform_configuration = self.platforms().get_platform(platform_name)
                except ValueError as e:
                    print str(e)
                    continue
                # Make steps for build factory:
                # - Make checkout step.
                # - Update steps chain with builder-specific steps.
                # - Skip a configuration of the project if an error would occur.
                chain = [
                    Checkout(project_vcs, project_code, project.url(), branch_name, platform_name)
                ]
                try:
                    self.update_chain(chain, configuration, project, branch, platform_configuration)
                except Exception as e:
                    print str(e)
                    continue
                build_factory = util.BuildFactory()
                # Clean branch name to make it usable as a part of a builder name.
                branch_name = VCS.make(vcs=project_vcs).clean_branch_name(branch_name)
                # Make full builder name as 'pc-bn-pl'.
                builder_name = '-'.join([project_code, branch_name, platform_name])
                # Create builder config.
                builders.append(util.BuilderConfig(name=builder_name,
                                                   slavenames=platform_configuration.slaves(),
                                                   factory=build_factory))
        return builders

    def update_chain(self, chain, configuration, project, branch, platform):
        raise NotImplementedError()
