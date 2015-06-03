class Project:
    """
    ToDo add description
    """

    class ConfigurationException(Exception):

        def __init__(self, message):
            self.message = message

        def __str__(self):
            return self.message

    def __init__(self, project_name, project_path, project_type, description, updates):
        self._path = project_path
        self._name = project_name
        self._type = project_type
        self._description = description
        self._updates = updates

def make_project(project_name, project_path, project_data):
    """
    Creates an object that keeps information about project.

    :param project_path:
    :param project_name:
    :param project_type:
    :param project_data:
    :return:
    """

    info = project_data.get("info")
    updates = project_data.get("updates")

    if not info:
        raise Project.ConfigurationException("No 'info' section!")
    if not updates:
        raise Project.ConfigurationException("No 'updates' section!")
