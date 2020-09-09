import pytest
from django.conf import settings
from django.core.management import call_command

from muscles.models import Muscle, MuscleGrouping, MuscleSubportion
from tests.utils import get_json_file_len


def get_muscle_fixture_path():
    return settings.BASE_DIR / 'muscles' / 'fixtures'


@pytest.mark.django_db
def test_refresh_muscles_empty_db():
    num_subportions = get_json_file_len(get_muscle_fixture_path() / 'muscle_subportions.json')
    num_muscles = get_json_file_len(get_muscle_fixture_path() / 'muscles.json') + num_subportions
    num_groupings = get_json_file_len(get_muscle_fixture_path() / 'muscle_groupings.json') + num_muscles

    call_command('refresh_muscles')

    assert MuscleSubportion.objects.all().count() == num_subportions
    assert Muscle.objects.all().count() == num_muscles
    assert MuscleGrouping.objects.all().count() == num_groupings


@pytest.mark.django_db
def test_refresh_muscles_stale_db(muscle_grouping_factory):
    muscle_grouping_factory.create_batch(5)
    num_subportions = get_json_file_len(get_muscle_fixture_path() / 'muscle_subportions.json')
    num_muscles = get_json_file_len(get_muscle_fixture_path() / 'muscles.json') + num_subportions
    num_groupings = get_json_file_len(get_muscle_fixture_path() / 'muscle_groupings.json') + num_muscles

    call_command('refresh_muscles')

    assert MuscleSubportion.objects.all().count() == num_subportions
    assert Muscle.objects.all().count() == num_muscles
    assert MuscleGrouping.objects.all().count() == num_groupings
