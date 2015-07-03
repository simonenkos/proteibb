class ExtensionMixin:
    """
    A mixin which implements extension functions such as 'include' and 'exclude'.
    Works only with such containers as 'list' or with object inherited from current mixin.
    """
    def include(self, value):
        extensible_object = None
        container = self._container()
        if not isinstance(container, list):
            extensible_object = container
        else:
            for elem in container:
                if elem == value:
                    extensible_object = elem
            if extensible_object is None:
                container.append(value)
        if extensible_object and isinstance(extensible_object, ExtensionMixin):
            extensible_object.include(extensible_object._strip(value))

    def exclude(self, value):
        container = self._container()
        if isinstance(container, list):
            for elem in container:
                if elem == value:
                    if isinstance(elem, ExtensionMixin):
                        if elem.exclude(elem._strip(value)):
                            container.remove(elem)
                    else:
                        container.remove(elem)
            return not len(container)
        if isinstance(container, ExtensionMixin):
            return container.exclude(value)
        return True

    def _container(self):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def _strip(self, value):
        # Current method will be called if extensible object is available for further extension.
        # Thus we need to get internal state of a value that used for extension to provide
        # type matching on a next layer.
        return value


class Extension:
    """
    An extension object is used to modify some other object according to
    some rules if that object implements 'ExtensionMixin' policy.
    """

    INCLUDE_MODIFICATION_FLAG = '+'
    EXCLUDE_MODIFICATION_FLAG = '-'

    def __init__(self, modification_flag, value):
        if modification_flag != Extension.INCLUDE_MODIFICATION_FLAG and \
           modification_flag != Extension.EXCLUDE_MODIFICATION_FLAG:
            raise ValueError('invalid value of a modification flag of an extension')
        self._modification_flag = modification_flag
        self._value = value

    def apply(self, extensible_object):
        if not isinstance(extensible_object, ExtensionMixin):
            raise TypeError('invalid object is used for extension')
        if self._modification_flag == Extension.INCLUDE_MODIFICATION_FLAG:
            extensible_object.include(self._value)
        else:
            extensible_object.exclude(self._value)

    def __eq__(self, other):
        if not isinstance(other, Extension):
            raise TypeError('invalid object type for extension comparison')
        return self._value == other._value and self._modification_flag == other._modification_flag