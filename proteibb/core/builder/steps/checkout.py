from buildbot import steps
from proteibb.util.factory import *

checkout_factory = NamedFactory('co')

class Checkout:

    def __init__(self):
        pass

    def make_step(self, configuration, url, branch):
        raise NotImplementedError()


@register_class(checkout_factory)
class Git(Checkout):

    def __init__(self):
        Checkout.__init__(self)

    def make_step(self, configuration, url, branch):
        return steps.Git(repourl=url, branch=branch, mode='full')


@register_class(checkout_factory)
class Svn(Checkout):

    def __init__(self):
        Checkout.__init__(self)

    def make_step(self, configuration, url, branch):
        return steps.SVN()


@register_class(checkout_factory)
class Hg(Checkout):

    def __init__(self):
        Checkout.__init__(self)

    def make_step(self, configuration, url, branch):
        return steps.Hg()