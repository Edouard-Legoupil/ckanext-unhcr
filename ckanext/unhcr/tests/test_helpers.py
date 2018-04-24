import os
from ckan import model
from ckan.tests import factories as core_factories
from nose.tools import assert_raises, assert_equals
from ckan.tests.helpers import call_action, FunctionalTestBase
from ckanext.unhcr.helpers import get_linked_datasets_for_form, get_linked_datasets_for_display
from ckanext.unhcr.tests import factories


class TestHelpers(FunctionalTestBase):

    # get_linked_datasets_for_form

    def test_get_linked_datasets_for_form_none(self):
        user = core_factories.User()
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_form(context=context, user_id=user['id'])
        assert_equals(linked_datasets, [])

    def test_get_linked_datasets_for_form_many(self):
        user = core_factories.User()
        container1 = factories.DataContainer(title='container1', users=[user])
        container2 = factories.DataContainer(title='container2', users=[user])
        dataset1 = factories.Dataset(id='id1', title='dataset1', owner_org=container1['id'])
        dataset2 = factories.Dataset(id='id2', title='dataset2', owner_org=container2['id'])
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_form(context=context, user_id=user['id'])
        assert_equals(linked_datasets, [
            {'text': 'container1', 'children': [{'text': 'dataset1', 'value': 'id1'}]},
            {'text': 'container2', 'children': [{'text': 'dataset2', 'value': 'id2'}]},
        ])

    def test_get_linked_datasets_for_form_many_selected_ids(self):
        user = core_factories.User(id='user_selected_ids', name='user_selected_ids')
        container1 = factories.DataContainer(title='container1', users=[user])
        container2 = factories.DataContainer(title='container2', users=[user])
        dataset1 = factories.Dataset(id='id1', title='dataset1', owner_org=container1['id'])
        dataset2 = factories.Dataset(id='id2', title='dataset2', owner_org=container2['id'])
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_form(context=context, user_id=user['id'], selected_ids=['id2'])
        assert_equals(linked_datasets, [
            {'text': 'container1', 'children': [{'text': 'dataset1', 'value': 'id1'}]},
            {'text': 'container2', 'children': [{'text': 'dataset2', 'value': 'id2', 'selected': 'selected'}]},
        ])

    def test_get_linked_datasets_for_form_many_exclude_ids(self):
        user = core_factories.User(id='user_exclude_ids', name='user_exclude_ids')
        container1 = factories.DataContainer(title='container1', users=[user])
        container2 = factories.DataContainer(title='container2', users=[user])
        dataset1 = factories.Dataset(id='id1', title='dataset1', owner_org=container1['id'])
        dataset2 = factories.Dataset(id='id2', title='dataset2', owner_org=container2['id'])
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_form(context=context, user_id=user['id'], exclude_ids=['id2'])
        assert_equals(linked_datasets, [
            {'text': 'container1', 'children': [{'text': 'dataset1', 'value': 'id1'}]},
        ])

    # get_linked_datasets_for_display

    def test_get_linked_datasets_for_display_none(self):
        user = core_factories.User()
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_display('', context=context)
        assert_equals(linked_datasets, [])

    def test_get_linked_datasets_for_display_one(self):
        url = os.environ.get('CKAN_SITE_URL', 'http://test.ckan.net')
        user = core_factories.User()
        dataset = factories.Dataset(name='name', title='title')
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_display(dataset['id'], context=context)
        assert_equals(linked_datasets, [
            {'href': '%s/dataset/name' % url, 'text': 'title'},
        ])

    def test_get_linked_datasets_for_display_many(self):
        url = os.environ.get('CKAN_SITE_URL', 'http://test.ckan.net')
        user = core_factories.User()
        dataset1 = factories.Dataset(name='name1', title='title1')
        dataset2 = factories.Dataset(name='name2', title='title2')
        context = {'model': model, 'user': user['name']}
        linked_datasets = get_linked_datasets_for_display(
            '{%s,%s}' % (dataset1['id'], dataset2['id']), context=context)
        assert_equals(linked_datasets, [
            {'href': '%s/dataset/name1' % url, 'text': 'title1'},
            {'href': '%s/dataset/name2' % url, 'text': 'title2'},
        ])
