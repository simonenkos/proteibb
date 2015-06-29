# Simple function to make version numbers array.
def split_version(ver):
    return [int(num) for num in ver.split('.')]

# Function to convert version list to string with underscore dividers.
def make_version(ver):
    return '_'.join([str(x) for x in ver])