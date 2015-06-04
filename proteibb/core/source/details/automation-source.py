from proteibb.core.source import *

class Automation(Source):

    def __init__(self, name, vcs, url):
        Source.__init__(self, name, vcs, url)

    def get_change_source(self):
        raise NotImplementedError()

    def get_sources(self):
        raise NotImplementedError()

@add_source_factory("automation")
def make_automation_sources(data):
    pass


