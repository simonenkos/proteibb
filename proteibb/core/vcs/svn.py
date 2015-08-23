from proteibb.core.vcs.vcs import VCS
from proteibb.util.factory import register_class

from buildbot.plugins import changes, steps, util


@register_class(VCS.factory)
class Svn(VCS):

    def checkout(self, configuration, url, branch, work_dir, *args, **kwargs):
        return steps.Svn(repourl=Svn._make_url(url, branch),
                         mode='full',
                         workdir=work_dir,
                         username=configuration.svnuser(),
                         password=configuration.svnpass())

    def change_source(self, project, configuration, *args, **kwargs):
        cs_list = []
        for branch in project.branches():
            cs = changes.SVNPoller(svnurl=Svn._make_url(project.url(), branch),
                                   split_file=util.svn.split_file_branches,
                                   project=project.name(),
                                   svnuser=configuration.svnuser(),
                                   svnpasswd=configuration.svnpass())
            cs_list.append(cs)
        return cs_list

    def clean_branch_name(self, branch):
        if branch != 'trunk':
            branch = branch.split('/').pop()
        return branch

    @staticmethod
    def _make_url(url, branch):
        if not url.endswith('/'):
            url = '/'
        return url + branch
