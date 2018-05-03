def normalize_list(value):
    if isinstance(value, list):
        return value
    value = value.strip('{}')
    if value:
        return value.split(',')
    return []
