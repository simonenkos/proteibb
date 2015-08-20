import os.path

from buildbot.plugins import steps
from proteibb.core.builder.step import Step
from proteibb.util.factory import NamedFactory, register_class


class Checkout(Step):
    """
    Class provide methods to create buildbot step for checkout operation.
    """
    class ImplementationFactory(NamedFactory):

        def __init__(self):
            NamedFactory.__init__(self, 'vcs')

    def __init__(self, vcs, code, url, branch, platform):
        work_dir = os.path.join(code, branch, platform)
        step_callback = lambda: Checkout.ImplementationFactory().make(vcs=vcs, url=url, branch=branch,
                                                                      work_dir=work_dir)
        data_callback = lambda: work_dir
        Step.__init__(self, data_callback, step_callback)


@register_class(Checkout.ImplementationFactory)
def git(url, branch, work_dir):
    return steps.Git(repourl=url, branch=branch, mode='full', workdir=work_dir)

