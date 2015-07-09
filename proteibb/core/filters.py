import os.path

from proteibb.util import *
from proteibb.util.filter import *
from buildbot.plugins import *

class ConfigurationFilter(Filter):

    def __init__(self, conf_name):
        Filter.__init__(self, lambda conf: type(conf).__name__.lower() == conf_name,
                        ConfigurationFilter._altering_function)

    @staticmethod
    def _altering_function(conf_list):
        if len(conf_list) != 1:
            raise ValueError('unexpected filtered configuration objects count')
        return conf_list[0]

class TypeFilter(Filter):

    def __init__(self, desired_project_type):
        Filter.__init__(self, lambda project: project.type() == desired_project_type)

class VcsFilter(Filter):

    def __init__(self, desired_project_vcs):
        Filter.__init__(self, lambda project: project.vsc() == desired_project_vcs, self.make_change_sources)

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

    def __init__(self):
        VcsFilter.__init__(self, 'svn')

    def change_source(self, project):
        cs_list = []
        url = project.url()
        if not url.endswith('/'):
            url += '/'
        for branch in project.branches():
            cs = changes.SVNPoller(svnurl=(url + branch.name()),
                                   split_file=util.svn.split_file_branches,
                                   project=project.name())
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
