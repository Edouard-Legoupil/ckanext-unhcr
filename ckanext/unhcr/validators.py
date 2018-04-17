import logging
from ckan.plugins.toolkit import Invalid
log = logging.getLogger(__name__)


def linked_datasets(value, context):
    log.debug('Validator: linked_datasets')
    if not value:
        raise Invalid()
    return value
