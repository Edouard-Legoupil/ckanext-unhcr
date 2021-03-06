import logging
from ckan.plugins import toolkit
from ckan.plugins.toolkit import Invalid
from ckanext.unhcr.helpers import get_linked_datasets_for_form
from ckanext.unhcr import utils
log = logging.getLogger(__name__)


# Module API

def ignore_if_attachment(key, data, errors, context):
    index = key[1]
    if _is_attachment(index, data):
        data.pop(key, None)
        raise toolkit.StopOnError


def linked_datasets(value, context):
    if context.get('job'):
        return value

    # Check if the user has access to the linked datasets
    selected = utils.normalize_list(value)
    allowed = _get_allowed_linked_datasets()
    for id in selected:
        if id not in allowed:
            raise Invalid('Invalid linked datasets')

    return value


# Internal

def _is_attachment(index, data):
    for field, value in data.iteritems():
        if (field[0] == 'resources' and
                field[1] == index and
                field[2] == 'type' and
                value == 'attachment'):
            return True
    return False


# TODO:
# it could be better to extract core linked datasets
# preparing function to use here and in the helpers
def _get_allowed_linked_datasets():
    datasets = []
    for container in get_linked_datasets_for_form():
        for dataset in container['children']:
            datasets.append(dataset['value'])
    return datasets
