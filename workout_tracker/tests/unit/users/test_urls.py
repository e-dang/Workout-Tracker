from tests.utils import add_api_prefix
from rest_framework.reverse import reverse


def test_user_list_url():
    assert reverse('user-list') == add_api_prefix('users/')


def test_user_detail_url():
    pk = 1
    assert reverse('user-detail', kwargs={'pk': 1}) == add_api_prefix(f'users/{pk}/')
