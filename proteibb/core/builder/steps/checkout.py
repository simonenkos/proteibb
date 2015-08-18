from buildbot import steps

from proteibb.core.builder.step import Step

class Checkout(Step):
    """
    Class provide methods to create buildbot step for checkout operation.
    """
    def __init__(self, name, configuration, url, branch, path):
        maker = getattr(self, '_' + name + '_maker')
        if not maker:
            raise ValueError('no checkout provided for: ' + name)
        step_callback = lambda: maker(configuration, url, branch)
        data_callback = lambda: path
        Step.__init__(self, data_callback, step_callback)

    def _git_maker(self, configuration, url, branch):
        return steps.Git(repourl=url, branch=branch, mode='full')

    def _svn_maker(self, configuration, url, branch):
        return steps.SVN(repourl=url, branch=branch, mode='full')

    def _hg_maker(self, configuration, url, branch):
        return steps.Hg(repourl=url, branch=branch, mode='full')
