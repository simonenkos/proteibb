
class BuildManager:

    """Build manager initialises a structure of the build system and make
    some processing blocks to pass them into buildbot.
    """

    def __init__(self):
        pass

    def getSlaves(self):
        pass

    def getChangeSources(self):
        pass

    def getSchedulers(self):
        pass

    def getBuilders(self):
        pass

    def getStatusTargets(self):
        pass


'''

'''
def initializeBuildManager(build_manager_root_path):
    bm = BuildManager()
    return bm
