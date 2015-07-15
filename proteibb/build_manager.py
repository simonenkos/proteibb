import proteibb.core.workspace as ws
import proteibb.core.filters as filters

class BuildManager:
    """Build manager initialises a structure of the build system and make
    some processing blocks to pass them into buildbot.
    """

    def __init__(self, ws_root_path):
        self._ws = ws.Workspace(ws_root_path)

    def get_slaves(self):
        configuration = self._ws.get_configuration(filters.ConfigurationFilter)
        slaves_list = []
        for slave in configuration.slaves():
            slaves_list.append(slave.make())
        return slaves_list

    def get_change_sources(self):
        library_filter = filters.TypeFilter('library')
        libraries = self._ws.get_projects(library_filter)
        configuration = self._ws.get_configuration(filters.ConfigurationFilter)
        cs_filter = filters.apply_filter_set_parallel(filters.GitFilter(),
                                                      filters.SvnFilter(configuration),
                                                      filters.HgFilter())
        return cs_filter(libraries)

    def get_schedulers(self):
        pass

    def get_builders(self):
        builders = []
        configuration = self._ws.get_configuration(filters.ConfigurationFilter)
        library_filter = filters.TypeFilter('library')
        for lib in self._ws.get_projects(library_filter):
            # ToDo make this code works
            builder = self._ws.get_builders(filters.NameFilter(lib.builder()))
            builders.extend(builder.make(configuration, lib))

    def get_status_targets(self):
        pass
