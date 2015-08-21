import os.path

from proteibb.core.builder.step import Step
from proteibb.core.vcs.vcs import VCS


class Checkout(Step):
    """
    Class provide methods to create buildbot step for checkout operation.
    """
    def __init__(self, vcs, code, url, branch, platform):
        self._work_dir = os.path.join(code, branch, platform)
        self._checkout = VCS.make(vcs=vcs).checkout(url, branch, self._work_dir)

    def setup(self, *args, **kwargs):
        # Do nothing.
        pass

    def data(self):
        return self._work_dir

    def step(self):
        return self._checkout

