from proteibb.util.filter import *

class TypeFilter(Filter):

    def __init__(self, desired_project_type):
        Filter.__init__(self, lambda project: project.type() == desired_project_type)

class VcsFilter(Filter):

    def __init__(self, desired_vcs_type):
        Filter.__init__(self, lambda project: project.vcs() == desired_vcs_type)
