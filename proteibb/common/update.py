class Update:

    """
    Class describes update entry from updates.json at a project.
    """

    def __init__(self, url, update_type, revision):
        self._url = url
        self._type = update_type
        self._revision = revision


def make_update_list():
    pass
