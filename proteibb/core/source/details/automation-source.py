from proteibb.core.source import *
from copy import *

class Automation(Source):

    def __init__(self, data, details):
        Source.__init__(self, data, details)
        # self._name.set_value(data[self._name.get_name()])
        # for details_entry in details:

    def get_change_source(self):
        raise NotImplementedError()

    def get_sources(self):
        raise NotImplementedError()

# @add_source_factory
# def make_automation_sources(data):
#     sources = []
#     details = data['automation']
#     for details_entry in details:
#         src = Automation()
#         src.parse_common_source_details(data)
#         src.parse_common_source_details(details_entry)
#         sources.append(deepcopy(src))
#     return sources
