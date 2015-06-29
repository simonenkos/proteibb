from proteibb.util.filter import *
from buildbot.plugins import *

class TypeFilter(Filter):

    def __init__(self, desired_project_type):
        Filter.__init__(self, lambda project: project.type() == desired_project_type)

class VcsFilter(Filter):

    def __init__(self, desired_project_vcs):
        Filter.__init__(self, lambda project: project.vsc() == desired_project_vcs, VcsFilter.make_change_sources)

    @staticmethod
    def make_change_sources(vcs_list):
        cs_list = []
        for vcs in vcs_list:
            p = VcsFilter.make(vcs)
            cs_list.append(p)
        return cs_list

    @staticmethod
    def change_source(vcs):
        raise NotImplementedError()

class GitFilter(VcsFilter):

    def __init__(self):
        VcsFilter.__init__(self, 'git')

    @staticmethod
    def change_source(vcs):
        return changes.GitPoller() # ToDo
