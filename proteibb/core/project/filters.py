import os.path

from proteibb.util import *
from proteibb.core.filters import *
from proteibb.core.configuration import configuration as conf
from proteibb.core.project.project import Project
from buildbot.plugins import *


class ProjectFilter(Filter):

    def __init__(self, filter_function, altering_function=None):
        def check(project):
            if not isinstance(project, Project):
                raise TypeError('invalid object was passed to project filtering function')
            return filter_function(project)
        Filter.__init__(self, check, altering_function)


class TypeFilter(ProjectFilter):

    def __init__(self, desired_project_type):
        ProjectFilter.__init__(self, lambda project: project.type() == desired_project_type)


class VcsFilter(ProjectFilter):

    def __init__(self, desired_project_vcs):
        ProjectFilter.__init__(self, lambda project: project.vsc() == desired_project_vcs, self.make_change_sources)

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
        raise NotImplementedError()


class GitFilter(VcsFilter):

    def __init__(self):
        VcsFilter.__init__(self, 'git')

    def change_source(self, project):
        branch_list = [branch.name() for branch in project.branches()]
        return changes.GitPoller(repourl=project.url(),
                                 branches=branch_list,
                                 project=project.name())


class SvnFilter(VcsFilter):

    def __init__(self, configuration):
        if not isinstance(configuration, conf.Configuration):
            raise TypeError('invalid configuration object was passed to svn filter')
        self._configuration = configuration
        VcsFilter.__init__(self, 'svn')

    def change_source(self, project):
        cs_list = []
        url = project.url()
        if not url.endswith('/'):
            url += '/'
        for branch in project.branches():
            cs = changes.SVNPoller(svnurl=(url + branch.name()),
                                   split_file=util.svn.split_file_branches,
                                   project=project.name(),
                                   svnuser=self._configuration.svnuser(),
                                   svnpasswd=self._configuration.svnpass())
            cs_list.append(cs)
        return cs_list


class HgFilter(VcsFilter):

    def __init__(self):
        VcsFilter.__init__(self, 'hg')

    def change_source(self, project):
        cs_list = []
        for branch in project.branches():
            work_dir = os.path.join(project.name(),
                                    make_version(branch.version()),
                                    branch.name())
            cs = changes.HgPoller(repourl=project.url(),
                                  branch=branch.name(),
                                  workdir=work_dir)
            cs_list.append(cs)
        return cs_list
