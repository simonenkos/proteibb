from proteibb.util.filter import *
# from proteibb.core.project import project

class TypeFilter(Filter):

    def __init__(self, desired__project_type):
        Filter.__init__(self, lambda project: project.type() == desired__project_type)

class VcsFilter(Filter):

    def __init__(self, desired_vcs_type):
        Filter.__init__(self, lambda project: project.vcs() == desired_vcs_type)

    def __call__(self, *args, **kwargs):
        projects = Filter.__call__(*args, **kwargs)

        def apply(url, suffix):
            if not url.endswith('/'):
                url += '/'
            url += suffix

        for p in projects:
            pass # ToDo
            # brances = p.branches()
            # for b in brances:
            # versions = p.versions()

    def _make_poller(self, project):
        raise NotImplementedError()

class Git(VcsFilter):

    def __init__(self):
        VcsFilter.__init__(self, 'git')

    def _make_poller(self, project):
        pass
