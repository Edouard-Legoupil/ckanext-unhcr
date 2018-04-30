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


def process_dataset_links_on_create(data_dict):
    _create_back_references_on_linked_datasets(data_dict)


def process_dataset_links_on_delete(data_dict):
    _delete_back_references_from_linked_datasets(data_dict)


def process_dataset_links_on_update(data_dict):
    _update_back_references_on_linked_datasets(data_dict)


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


def _create_back_references_on_linked_datasets(data_dict, whitelist=None):
    context = {'model': model, 'job': True}
    package_id = data_dict['id']
    for link_package_id in utils.normalize_list(data_dict.get('linked_datasets', [])):
        if whitelist is not None and link_package_id not in whitelist:
            continue
        link_package = toolkit.get_action('package_show')(context, {'id': link_package_id})
        back_package_ids = utils.normalize_list(link_package.get('linked_datasets', []))
        if package_id not in back_package_ids:
            link_package['linked_datasets'] = back_package_ids + [package_id]
            toolkit.get_action('package_update')(context, link_package)


def _delete_back_references_from_linked_datasets(data_dict, whitelist=None):
    context = {'model': model, 'job': True}
    package_id = data_dict['id']
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


def _update_back_references_on_linked_datasets(data_dict):
    context = {'model': model, 'job': True}

    # Prepare
    package_id = data_dict['id']
    package = toolkit.get_action('package_show')(context, {'id': package_id})
    # TODO: it doesn't work because the following lists are always the same
    old_link_package_ids = utils.normalize_list(package.get('linked_datasets', []))
    new_link_package_ids = utils.normalize_list(data_dict.get('linked_datasets', []))

    # Create
    created_link_package_ids = set(new_link_package_ids).difference(old_link_package_ids)
    if created_link_package_ids:
        _create_back_references_on_linked_datasets(data_dict, whitelist=created_link_package_ids)

    # Delete
    removed_link_package_ids = set(old_link_package_ids).difference(new_link_package_ids)
    if removed_link_package_ids:
        _delete_back_references_from_linked_datasets({'id': package_id}, whitelist=removed_link_package_ids)
