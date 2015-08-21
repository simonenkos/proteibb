from proteibb.util.factory import NamedFactory


class VCS:

    def checkout(self, *args, **kwargs):
        raise NotImplementedError()

    def change_source(self, *args, **kwargs):
        raise NotImplementedError()

    factory = NamedFactory('vcs')

    @staticmethod
    def make(*args, **kwargs):
        return VCS.factory.make(*args, **kwargs)
