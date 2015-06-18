from proteibb.util.simple_factory import SimpleFactory

class DetailsFactory(SimpleFactory):

    def __init__(self):
        SimpleFactory.__init__(self)

    def make(self, project_type, *args, **kwargs):
        for cls in self._registry:
            if cls.__name__.tolower() == project_type:
                return cls(*args, **kwargs)
        return None

details_factory = DetailsFactory()
