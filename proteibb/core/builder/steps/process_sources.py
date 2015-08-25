from buildbot import steps

from proteibb.core.builder.step import Step

class ProcessSources(Step):

    def __init__(self, project, file_filter):
        # Find all files for compilation step.
        # Make directories.
        # Use different steps?
        self._project = project

    def setup(self, work_dir, *args, **kwargs):
        pass

    def data(self):
        pass

    def step(self):
        pass
