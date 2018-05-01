import logging
from ckan import model
from ckanext.unhcr import utils
import ckan.plugins.toolkit as toolkit
log = logging.getLogger(__name__)


# Module API

def process_dataset_fields(package_id):

    # Get package
    package_show = toolkit.get_action('package_show')
    package = package_show({'job': True}, {'id': package_id})

    # Modify package
    package = _modify_package(package)

    # Update package
    package_update = toolkit.get_action('package_update')
    package_update({'job': True}, package)


def process_dataset_links_on_create(package_id, whitelist=None):
    context = {'model': model, 'job': True}
    package = toolkit.get_action('package_show')(context, {'id': package_id})
    for link_package_id in utils.normalize_list(package.get('linked_datasets', [])):
        if whitelist is not None and link_package_id not in whitelist:
            continue
        link_package = toolkit.get_action('package_show')(context, {'id': link_package_id})
        back_package_ids = utils.normalize_list(link_package.get('linked_datasets', []))
        if package_id not in back_package_ids:
            link_package['linked_datasets'] = back_package_ids + [package_id]
            toolkit.get_action('package_update')(context, link_package)


def process_dataset_links_on_delete(package_id, whitelist=None):
    context = {'model': model, 'job': True}
    package = toolkit.get_action('package_show')(context, {'id': package_id})
    for link_package_id in utils.normalize_list(package.get('linked_datasets', [])):
        if whitelist is not None and link_package_id not in whitelist:
            continue
        link_package = toolkit.get_action('package_show')(context, {'id': link_package_id})
        back_package_ids = utils.normalize_list(link_package.get('linked_datasets', []))
        if package_id in back_package_ids:
            back_package_ids.remove(package_id)
            link_package['linked_datasets'] = back_package_ids
            toolkit.get_action('package_update')(context, link_package)


def process_dataset_links_on_update(package_id, prev_package):
    context = {'model': model, 'job': True}

    # Prepare
    next_package = toolkit.get_action('package_show')(context, {'id': package_id})
    prev_link_package_ids = utils.normalize_list(prev_package.get('linked_datasets', []))
    next_link_package_ids = utils.normalize_list(next_package.get('linked_datasets', []))
    created_link_package_ids = set(next_link_package_ids).difference(prev_link_package_ids)
    removed_link_package_ids = set(prev_link_package_ids).difference(next_link_package_ids)

    # Create
    if created_link_package_ids:
        process_dataset_links_on_create(package_id, whitelist=created_link_package_ids)

    # Delete
    if removed_link_package_ids:
        process_dataset_links_on_delete(package_id, whitelist=removed_link_package_ids)


# Internal

def _modify_package(package):

    # data_range
    package = _modify_date_range(package, 'date_range_start', 'date_range_end')

    # process_status
    weights = {'raw' : 3, 'in_process': 2, 'final': 1}
    package = _modify_weighted_field(package, 'process_status', weights)

    # identifiability
    weights = {'personally_identifiable' : 2, 'anonymized': 1}
    package = _modify_weighted_field(package, 'identifiability', weights)

    # private
    if package['identifiability'] == 'personally_identifiable':
        package['private'] = True

    return package


def _modify_date_range(package, key_start, key_end):
    # Reset for generated
    package[key_start] = None
    package[key_end] = None
    for resource in package['resources']:
        if resource.get(key_start, resource.get(key_end)) is None:
            continue
        # We could compare dates as strings because it's guarnateed to be YYYY-MM-DD
        package[key_start] = min(filter(None, [package[key_start], resource[key_start]]))
        package[key_end] = max(filter(None, [package[key_end], resource[key_end]]))
    return package


def _modify_weighted_field(package, key, weights):
    # Reset for generated
    package[key] = None
    for resource in package['resources']:
        if resource.get(key) is None:
            continue
        package_weight = weights.get(package[key], 0)
        resource_weight = weights.get(resource[key], 0)
        if resource_weight > package_weight:
            package[key] = resource[key]
    return package
