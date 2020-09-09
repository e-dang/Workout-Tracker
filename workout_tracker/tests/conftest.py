import pytest
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from . import factories


@pytest.fixture(scope='session')
def faker_seed():
    return 12345


register(factories.UserFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return factories.TEST_PASSWORD


@pytest.fixture
def auto_login_user(db, api_client, user_factory):
    def make_auto_login(user=None, **kwargs):
        if user is None:
            user = user_factory(**kwargs)
        token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return api_client, user

    return make_auto_login


def _get_test_type(item):
    """
    Gets the test type - unit, functional, integration, based on the directory that the test is in.
    """

    return item.nodeid.split('/')[1]


def _sort_key(item):
    """
    Used has the key to sort functions based on their marks, where the ordering is unit -> functional -> integration
    """

    key_dict = {
        pytest.mark.unit.name: 1,
        pytest.mark.functional.name: 2,
        pytest.mark.integration.name: 3
    }
    names = [pytest.mark.unit.name,
             pytest.mark.functional.name,
             pytest.mark.integration.name]

    for mark in item.own_markers:
        if mark.name in names:
            return key_dict[mark.name]


def pytest_collection_modifyitems(items):
    """
    Adds unit, functional, or integration test marks to each test based on the directory it is in and then sorts the
    tests so that unittests are executed first, then functional tests, followed by integration tests.
    """

    # apply marks
    for item in items:
        test_type = _get_test_type(item)
        if test_type == 'unit':
            item.add_marker(pytest.mark.unit)
        elif test_type == 'functional':
            item.add_marker(pytest.mark.functional)
        elif test_type == 'integration':
            item.add_marker(pytest.mark.integration)

    # change order of test execution
    items.sort(key=_sort_key)
