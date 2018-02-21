import ckan.plugins.toolkit as toolkit


def process_dataset_fields(package_id):

    # Get package
    package_show = toolkit.get_action('package_show')
    package = package_show({}, {'id': package_id})

    # Modify package
    package = _modify_package(package)

    # Update package
    package_update = toolkit.get_action('package_update')
    package_update({}, package)


def _modify_package(package):

    # data_range
    package = _modify_date_range(package, 'date_range_start', 'date_range_end')

    # process_status
    default = 'raw'
    weights = {'raw' : 3, 'in_process': 2, 'final': 1}
    package = _modify_weighted_field(package, 'process_status', weights)
    package = _modify_required_field(package, 'process_status', default)

    # identifiability
    default = 'personally_identifiable'
    weights = {'personally_identifiable' : 2, 'anonymized': 1}
    package = _modify_weighted_field(package, 'identifiability', weights)
    package = _modify_required_field(package, 'identifiability', default)

    # raw_access_data_level
    default = 'private'
    package = _modify_required_field(package, 'raw_access_data_level', default)
    if package['identifiability'] == 'personally_identifiable':
        package['raw_access_data_level'] = 'private'

    # private
    package['private'] = package['raw_access_data_level'] == 'private'

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


def _modify_required_field(package, key, default):
    package[key] = package.get(key) or default
    return package
