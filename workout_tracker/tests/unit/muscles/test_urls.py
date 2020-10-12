from rest_framework.reverse import reverse
from tests.utils import add_api_prefix


def test_muscles_list_url():
    assert reverse('muscle-list') == add_api_prefix('muscles/')


def test_muscles_detail_url():
    pk = 1
    assert reverse('muscle-detail', kwargs={'pk': pk}) == add_api_prefix(f'muscles/{pk}/')
