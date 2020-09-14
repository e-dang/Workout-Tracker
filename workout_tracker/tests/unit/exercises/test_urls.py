from rest_framework.reverse import reverse
from tests.utils import add_api_prefix


def test_exercise_template_list_url():
    assert reverse('exercise-list') == add_api_prefix('exercises/')


def test_exercise_template_detail_url():
    pk = 1
    assert reverse('exercise-detail', kwargs={'pk': pk}) == add_api_prefix(f'exercises/{pk}/')


def test_user_exercise_template_list_url():
    pk = 1
    assert reverse('user-exercise-list', kwargs={'pk': pk}) == add_api_prefix(f'users/{pk}/exercises/')
