# Simple function to make version numbers array.
def split_version(ver):
    return [int(num) for num in ver.split('.')]
