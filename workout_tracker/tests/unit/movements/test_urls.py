from rest_framework.reverse import reverse
from tests.utils import add_api_prefix


def test_movements_list_url():
    assert reverse('movement-list') == add_api_prefix('movements/')


def test_movements_detail_url():
    pk = 1
    assert reverse('movement-detail', kwargs={'pk': pk}) == add_api_prefix(f'movements/{pk}/')


def test_user_movements_list_url():
    pk = 1
    assert reverse('user-movement-list', kwargs={'pk': pk}) == add_api_prefix(f'users/{pk}/movements/')
