from buildbot import steps

from proteibb.core.builder.step import Step

class Checkout(Step):
    """
    Class provide methods to create buildbot step for checkout operation.
    """
    def __init__(self, name):
        self._name = name

    def get_step(self, configuration, url, branch):
        maker = getattr(self, '_' + self._name + '_maker')
        if not maker:
            raise ValueError('No checkout provided for: ' + self._name)
        return maker(configuration, url, branch)

    def _git_maker(self, configuration, url, branch):
        return steps.Git(repourl=url, branch=branch, mode='full')

    def _svn_maker(self, configuration, url, branch):
        return steps.SVN(repourl=url, branch=branch, mode='full') # ToDo

    def _hg_maker(self, configuration, url, branch):
        return steps.Hg(repourl=url, branch=branch, mode='full') # ToDo
