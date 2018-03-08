import pylons
from paste.registry import Registry

from nose.tools import assert_in, assert_not_in
from ckan.tests import helpers
from ckan.tests import factories as core_factories

from ckanext.unhcr.tests import factories


class TestAuthUI(helpers.FunctionalTestBase):

    @classmethod
    def setup_class(cls):

        super(TestAuthUI, cls).setup_class()

        # Hack because the hierarchy extension uses c in some methods
        # that are called outside the context of a web request
        c = pylons.util.AttribSafeContextObj()
        registry = Registry()
        registry.prepare()
        registry.register(pylons.c, c)

    def test_non_logged_in_users(self):

        app = self._get_test_app()

        dataset = factories.Dataset()
        data_container = factories.DataContainer()

        endpoints = [
            '/',
            '/dataset',
            '/dataset/{}'.format(dataset['name']),
            '/data-container',
            '/data-container/{}'.format(data_container['name']),
        ]
        for endpoint in endpoints:
            response = app.get(endpoint)
            assert_in('You must be logged in', response.body)

    def test_logged_in_users(self):

        app = self._get_test_app()

        user = core_factories.User()
        dataset = factories.Dataset()
        data_container = factories.DataContainer()

        endpoints = [
            '/',
            '/dataset',
            '/dataset/{}'.format(dataset['name']),
            '/data-container',
            '/data-container/{}'.format(data_container['name']),
        ]

        environ = {
            'REMOTE_USER': str(user['name'])
        }

        for endpoint in endpoints:
            response = app.get(endpoint, extra_environ=environ)
            assert_not_in('You must be logged in', response.body)

    def test_logged_in_users_private_dataset(self):

        app = self._get_test_app()

        user1 = core_factories.User()
        user2 = core_factories.User()
        data_container = factories.DataContainer(
            users=[{'name': user1['name'], 'capacity': 'admin'}]
        )
        dataset = factories.Dataset(
            owner_org=data_container['id'],
            private=True
        )

        environ = {
            'REMOTE_USER': str(user1['name'])
        }

        response = app.get(
            '/dataset/{}'.format(dataset['name']), extra_environ=environ)
        assert_not_in('You must be logged in', response.body)

        environ = {
            'REMOTE_USER': str(user2['name'])
        }

        response = app.get(
            '/dataset/{}'.format(dataset['name']), extra_environ=environ,
            status=404)
