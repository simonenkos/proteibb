import proteibb.core.workspace as ws
import proteibb.core.filters as filters

class BuildManager:
    """Build manager initialises a structure of the build system and make
    some processing blocks to pass them into buildbot.
    """

    def __init__(self, ws_root_path):
        self._ws = ws.Workspace(ws_root_path)

    def get_slaves(self):
        pass

    def get_change_sources(self):
        library_filter = filters.TypeFilter('library')
        libraries = self._ws.get_projects(library_filter)
        cs_filter = filters.apply_filter_set_parallel(filters.GitFilter(),
                                                      filters.SvnFilter(),
                                                      filters.HgFilter())
        return cs_filter(libraries)

    def get_schedulers(self):
        pass

    def get_builders(self):
        pass

    def get_status_targets(self):
        pass
