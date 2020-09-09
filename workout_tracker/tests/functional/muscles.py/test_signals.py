import pytest
from muscles.models import MuscleSubportion, Muscle, MuscleGrouping


@pytest.mark.django_db
def test_grouping_creation():
    muscle = MuscleGrouping.objects.create(name='test_name', snames=['test_name1', 'test_name2'])

    assert MuscleSubportion.objects.all().count() == 0
    assert Muscle.objects.all().count() == 0


@pytest.mark.django_db
def test_muscle_to_grouping_creation():
    muscle = Muscle.objects.create(name='test_name', snames=['test_name1', 'test_name2'])

    assert MuscleSubportion.objects.all().count() == 0
    assert muscle.groupings.all().count() == 1
    grouping = muscle.groupings.all()[0]
    assert grouping.name == muscle.name
    assert grouping.snames == muscle.snames


@pytest.mark.django_db
def test_subportion_to_grouping_creation():
    subportion = MuscleSubportion.objects.create(name='test_name', snames=['test_name1', 'test_name2'])

    assert subportion.muscles.all().count() == 1
    muscle = subportion.muscles.all()[0]
    assert subportion.name == muscle.name
    assert subportion.snames == muscle.snames
    assert muscle.groupings.all().count() == 1
    grouping = muscle.groupings.all()[0]
    assert grouping.name == muscle.name
    assert grouping.snames == muscle.snames


@pytest.mark.django_db
def test_empty_relationship_clean_up_from_grouping():
    subportion = MuscleSubportion.objects.create(name='test_name', snames=['test_name1', 'test_name2'])
    grouping = subportion.muscles.last().groupings.last()

    grouping.delete()

    assert MuscleSubportion.objects.all().count() == 1
    assert Muscle.objects.all().count() == 1
    assert MuscleGrouping.objects.all().count() == 0


@pytest.mark.django_db
def test_empty_relationship_clean_up_from_muscle():
    subportion = MuscleSubportion.objects.create(name='test_name', snames=['test_name1', 'test_name2'])
    muscle = subportion.muscles.last()

    muscle.delete()

    assert MuscleSubportion.objects.all().count() == 1
    assert Muscle.objects.all().count() == 0
    assert MuscleGrouping.objects.all().count() == 0


@pytest.mark.django_db
def test_empty_relationship_clean_up_from_subportion():
    subportion = MuscleSubportion.objects.create(name='test_name', snames=['test_name1', 'test_name2'])

    subportion.delete()

    assert MuscleSubportion.objects.all().count() == 0
    assert Muscle.objects.all().count() == 0
    assert MuscleGrouping.objects.all().count() == 0
