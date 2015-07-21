import proteibb.core.workspace as ws
import proteibb.core.filters as filters
import proteibb.core.project.filters as project_filters

class BuildManager:
    """Build manager initialises a structure of the build system and make
    some processing blocks to pass them into buildbot.
    """

    def __init__(self, ws_root_path):
        self._ws = ws.Workspace(ws_root_path)

    def get_configuration(self):
        return self._ws.get_configuration(filters.ClassNameFilter('configuration'))

    def get_slaves(self):
        configuration = self.get_configuration()
        slaves_list = []
        for slave in configuration.slaves():
            slaves_list.append(slave.make())
        return slaves_list

    def get_change_sources(self):
        library_filter = project_filters.TypeFilter('library')
        libraries = self._ws.get_projects(library_filter)
        configuration = self._ws.get_configuration(filters.ClassNameFilter('configuration'))
        cs_filter = filters.apply_filter_set_parallel(project_filters.GitFilter(),
                                                      project_filters.SvnFilter(configuration),
                                                      project_filters.HgFilter())
        return cs_filter(libraries)

    def get_schedulers(self):
        pass

    def get_builders(self):
        builders = []
        configuration = self.get_configuration()
        for lib in self._ws.get_projects(filters.EmptyFiler):
            builder = self._ws.get_builders(filters.ClassNameFilter(lib.builder()))
            builders.extend(builder.make(configuration, lib))
        return builders

    def get_status_targets(self):
        pass
