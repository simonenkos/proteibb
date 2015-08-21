import os.path

from proteibb.core.vcs.vcs import VCS
from proteibb.util.factory import register_class

from buildbot.plugins import changes, steps


@register_class(VCS.factory)
class Hg(VCS):

    def checkout(self, url, branch, work_dir, *args, **kwargs):
        return steps.Mercurial(repourl=url, defaultBranch=branch, workdir=work_dir, mode='fresh')

    def change_source(self, project, *args, **kwargs):
        cs_list = []
        for branch in project.branches():
            work_dir = os.path.join(project.name(),
                                    branch.name())
            cs = changes.HgPoller(repourl=project.url(),
                                  branch=branch.name(),
                                  workdir=work_dir)
            cs_list.append(cs)
        return cs_list
