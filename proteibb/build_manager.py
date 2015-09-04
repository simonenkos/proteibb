import proteibb.core.workspace as ws
import proteibb.core.filters as filters
import proteibb.core.project.filters as project_filters

from proteibb.util.filter import apply_filter_set_parallel, apply_filter_set_serial


class BuildManager:
    """Build manager initialises a structure of the build system and make
    some processing blocks to pass them into buildbot.
    """

    def __init__(self, ws_root_path):
        self._ws = ws.Workspace(ws_root_path)
        try:
            self._ws.get_configuration(filters.ClassNameFilter('general'))
        except Exception as e:
            raise Exception("Can't load general.json configuration file: " + str(e))

    def get_slaves(self):
        configuration = self.get_configuration()
        slaves_list = []
        for slave in configuration.slaves():
            slaves_list.append(slave.make())
        return slaves_list

    def get_change_sources(self):
        library_filter = project_filters.TypeFilter('library')
        libraries = self._ws.get_projects(library_filter)
        configuration = self._ws.get_configuration(filters.ClassNameFilter('general'))
        cs_filter = apply_filter_set_parallel(project_filters.GitFilter(),
                                              project_filters.SvnFilter(configuration),
                                              project_filters.HgFilter())
        tmp = cs_filter(libraries)
        print "CSL=" + str(tmp)
        return tmp

    def get_schedulers(self):
        return []

    def get_builders(self):
        builders = []
        configuration = self._ws.get_configuration(filters.ClassNameFilter('general'))
        for project in self._ws.get_projects(filters.EmptyFiler()):
            builder = self._ws.get_builders(filters.ClassNameFilter(project.builder()))
            builders.extend(builder.make(configuration, project))
        return builders

    def get_status_targets(self):
        pass
