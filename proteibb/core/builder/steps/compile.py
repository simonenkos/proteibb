from buildbot import steps

from proteibb.core.builder.step import Step

class Compile(Step):

    def __init__(self):
        pass

    def get_step(self):
        return steps.ShellCommand()