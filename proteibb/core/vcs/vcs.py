from proteibb.util.factory import NamedFactory


class VCS:

    def __init__(self, *args, **kwargs):
        pass

    def checkout(self, *args, **kwargs):
        raise NotImplementedError()

    def change_source(self, *args, **kwargs):
        raise NotImplementedError()

    def clean_branch_name(self, branch):
        return branch.translate(None, ' ?.!/;:')

    factory = NamedFactory('vcs')

    @staticmethod
    def make(*args, **kwargs):
        return VCS.factory.make(*args, **kwargs)
