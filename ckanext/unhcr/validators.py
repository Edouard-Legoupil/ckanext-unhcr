import logging
from ckan.plugins.toolkit import Invalid
from ckanext.unhcr.helpers import get_linked_datasets_options
log = logging.getLogger(__name__)


def linked_datasets(value, context):

    # Check if the user has access to the linked datasets
    selected = value if isinstance(value, list) else value.strip('{}').split(',')
    allowed = [d['value'] for d in get_linked_datasets_options()]
    for id in selected:
        if id not in allowed:
            raise Invalid('Invalid linked datasets')

    return value
