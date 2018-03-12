from ckan.tests import factories


class Dataset(factories.Dataset):

    unit_of_measurement = 'individual'
    keywords = ['shelter', 'health']
    archived = 'False'
    source_organizations = ['un']
    data_collection_technique = 'interview'
    operational_purpose_of_data = 'idp_profiling'


class DataContainer(factories.Organization):

    type = 'data-container'

    country = 'south_africa'
    geographic_area = 'southern_africa'
    status = 'ok'
