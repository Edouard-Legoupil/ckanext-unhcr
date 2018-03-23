from ckan.plugins import toolkit


def _is_attachement(index, data):
    for field, value in data.iteritems():
        if (field[0] == 'resources' and
                field[1] == index and
                field[2] == 'type' and
                value == 'attachement'):
            return True
    return False


def ignore_if_attachement(key, data, errors, context):

    index = key[1]

    if _is_attachement(index, data):
        data.pop(key, None)
        raise toolkit.StopOnError
