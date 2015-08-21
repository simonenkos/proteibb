from proteibb.core.vcs.vcs import VCS
from proteibb.util.factory import register_class

from buildbot.plugins import changes, steps


@register_class(VCS.factory)
class Git(VCS):

    def checkout(self, url, branch, work_dir, *args, **kwargs):
        return steps.Git(repourl=url, branch=branch, mode='full', workdir=work_dir)

    def change_source(self, project, *args, **kwargs):
        branch_list = [branch.name() for branch in project.branches()]
        return changes.GitPoller(repourl=project.url(),
                                 branches=branch_list,
                                 project=project.name())
