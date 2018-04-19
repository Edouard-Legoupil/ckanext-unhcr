import logging
from ckan.plugins.toolkit import Invalid
from ckanext.unhcr import helpers
log = logging.getLogger(__name__)


def linked_datasets(value, context):

    # Check if the user has access to the linked datasets
    selected = value if isinstance(value, list) else value.strip('{}').split(',')
    allowed = [d['value'] for d in helpers.get_user_datasets(user_id=context['user'])]
    for id in selected:
        if id not in allowed:
            raise Invalid('Invalid linked datasets')

    return value
