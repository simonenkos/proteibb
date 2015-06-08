from proteibb.core.source import *
from copy import *

class Automation(Source):

    def __init__(self):
        Source.__init__(self)

    def get_change_source(self):
        raise NotImplementedError()

    def get_sources(self):
        raise NotImplementedError()

@add_source_factory
def make_automation_sources(data):
    sources = []
    details = data['automation']
    for details_entry in details:
        src = Automation()
        src.parse_common_source_details(data, Source.common_options)
        src.parse_common_source_details(details_entry, Source.specific_options)
        sources.append(deepcopy(src))
    return sources
