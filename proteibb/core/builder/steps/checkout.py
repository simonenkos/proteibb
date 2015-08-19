import os.path

from buildbot import steps
from proteibb.core.builder.step import Step
from proteibb.util.factory import NamedFactory
from proteibb.util import make_version

class Checkout(Step):

    class ImplementationFactory(NamedFactory):

        def __init__(self):
            NamedFactory.__init__(self, 'vcs')

    """
    Class provide methods to create buildbot step for checkout operation.
    """
    def __init__(self, vcs, configuration, code, url, branch, version):
        maker = getattr(self, '_' + vcs + '_maker')
        if not maker:
            raise ValueError('no checkout provided for: ' + vcs)
        work_dir = os.path.join(code, branch, make_version(version))
        step_callback = lambda: maker(configuration, url, branch)
        data_callback = lambda: work_dir
        Step.__init__(self, data_callback, step_callback)


class GitCheckout(Step):

    def __init__(self):
        make_callback = lambda: steps.Git(repourl=url, branch=branch, mode=full, workdir='')

        Step.__init__(self, None, make_callback)
    # def _git_maker(self, configuration, url, branch):
    #     return steps.Git(repourl=url, branch=branch, mode='full', workdir='')
    #
    # def _svn_maker(self, configuration, url, branch):
    #     return steps.SVN(repourl=url, branch=branch, mode='full')
    #
    # def _hg_maker(self, configuration, url, branch):
    #     return steps.Hg(repourl=url, branch=branch, mode='full')
