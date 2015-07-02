class ExtensibleMixin:
    """
    A mixin which implements extension functions such as 'include' and 'exclude'.
    Works only with such containers as 'list' or with object inherited from current mixin.
    """
    def __init__(self, container):
        self.__container = container

    def include(self, value):
        extensible_object = None
        if not isinstance(self.__container, list):
            extensible_object = self.__container
        else:
            for elem in self.__container:
                if elem == value:
                    extensible_object = elem
            if not extensible_object:
                self.__container.append(value)
        if extensible_object and isinstance(extensible_object, ExtensibleMixin):
            extensible_object.include(value)

    def exclude(self, value):
        if isinstance(self.__container, list):
            extensible_object = None
            for elem in self.__container:
                if elem == value:
                    extensible_object = elem
            if extensible_object is not None:
                if isinstance(extensible_object, ExtensibleMixin):
                    if extensible_object.exclude(value):
                        self.__container.remove(extensible_object)
                else:
                    self.__container.remove(extensible_object)
            return not len(self.__container)
        if isinstance(self.__container, ExtensibleMixin):
            return self.__container.exclude(value)
        return True
