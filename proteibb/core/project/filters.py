from proteibb.core.filters import *
from proteibb.core.configuration.general import General
from proteibb.core.project.project import Project
from proteibb.core.vcs.vcs import VCS


class ProjectFilter(AlteringFilter):

    def __init__(self, filter_function, altering_function=None, individual_altering=True):
        def check(project):
            if not isinstance(project, Project):
                raise TypeError('invalid object was passed to project filtering function')
            return filter_function(project)
        AlteringFilter.__init__(self, check, altering_function, individual_altering)


class TypeFilter(ProjectFilter):

    def __init__(self, desired_project_type):
        ProjectFilter.__init__(self, lambda project: project.type() == desired_project_type)


class VcsFilter(ProjectFilter):

    def __init__(self, desired_project_vcs):
        self._vcs_factory = VCS.make(vcs=desired_project_vcs)
        ProjectFilter.__init__(self, lambda project: project.vcs() == desired_project_vcs,
                               self.make_change_sources, False)

    def make_change_sources(self, project_list):
        cs_list = []
        for project in project_list:
            cs = self.change_source(project)
            try:
                iter(cs)
            except TypeError:
                cs_list.append(cs)
            else:
                cs_list.extend(cs)
        return cs_list

    def change_source(self, project):
        return self._vcs_factory.change_source(project)


class SvnFilter(VcsFilter):

    def __init__(self, configuration):
        # Require for 'General' configuration which should have svn authentication parameters.
        if not isinstance(configuration, General):
            raise TypeError('invalid configuration object was passed to svn filter')
        self._configuration = configuration
        VcsFilter.__init__(self, 'svn')

    def change_source(self, project):
        # Overload the function to have a possibility to pass the configuration as an argument.
        return self._vcs_factory.change_source(project, self._configuration)


class GitFilter(VcsFilter):

    def __init__(self):
        VcsFilter.__init__(self, 'git')


class HgFilter(VcsFilter):

    def __init__(self):
        VcsFilter.__init__(self, 'hg')
