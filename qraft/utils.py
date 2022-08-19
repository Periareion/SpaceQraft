
def validate_types(array, types):
    return (False not in [isinstance(x, types) for x in array])