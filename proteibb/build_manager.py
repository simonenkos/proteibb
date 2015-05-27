import proteibb.common.workspace as ws

class BuildManager:
    """Build manager initialises a structure of the build system and make
    some processing blocks to pass them into buildbot.
    """

    def __init__(self, bm_root_path):
        self._ws = ws.Workspace(bm_root_path)

    def get_slaves(self):
        pass

    def get_change_sources(self):
        pass

    def get_schedulers(self):
        pass

    def get_builders(self):
        pass

    def get_status_targets(self):
        pass