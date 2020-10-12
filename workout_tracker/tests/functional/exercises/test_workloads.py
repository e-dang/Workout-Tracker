import pytest

from exercises.models import Workload


@pytest.fixture(autouse=True)
def reset_set_sequence(set_factory, set_template_factory):
    set_factory.reset_sequence(0)
    set_template_factory.reset_sequence(0)
    yield


@pytest.mark.parametrize('factory, num_sets, idx', [
    (pytest.lazy_fixture('workload_factory'), 5, 1),
    (pytest.lazy_fixture('workload_template_factory'), 5, 1)
],
    ids=['workload', 'workload_template'])
@pytest.mark.django_db
def test_workload_delitem(factory, num_sets, idx):
    workload = factory(sets=num_sets)

    del workload[idx]

    sets = workload.sets.all()
    assert sets.count() == num_sets - 1
    assert [s.order for s in sets] == list(range(4))


@pytest.mark.parametrize('factory, num_sets, idx1, idx2', [
    (pytest.lazy_fixture('workload_factory'), 5, 4, 0),
    (pytest.lazy_fixture('workload_template_factory'), 5, 4, 0)
],
    ids=['workload', 'workload_template'])
@pytest.mark.django_db
def test_workload_swap_sets(factory, num_sets, idx1, idx2):
    workload = factory(sets=num_sets)
    sets = workload.sets.all()
    set1 = sets[idx1]
    set2 = sets[idx2]

    workload.swap_sets(idx1, idx2)

    sets = workload.sets.all()
    assert sets[idx1] == set2
    assert sets[idx2] == set1


@pytest.mark.parametrize('workload_factory, sets, reps, completed_reps, expected', [
    (None, 2, 10, 9, False),
    (None, 2, 10, 8, False),
    (None, 2, 10, 10, True),
    (None, 2, 10, 11, True)
],
    indirect=['workload_factory'],
    ids=['both_less_than', 'one_less_than', 'both_equal', 'both_greater_than'])
@pytest.mark.django_db
def test_workload_is_complete(workload_factory, sets, reps, completed_reps, expected):
    workload = workload_factory(sets=sets, sets__reps=reps, sets__completed_reps=completed_reps)
    if completed_reps == 8:
        workload.sets.last().completed_reps = reps

    assert workload.is_complete == expected


@pytest.mark.django_db
def test_workload_from_template(workload_template_factory, exercise_factory):
    num_sets = 5
    workload_template = workload_template_factory(sets=num_sets)
    exercise = exercise_factory()

    workload = Workload.from_template(workload_template, exercise)

    assert workload.sets.all().count() == num_sets
    assert workload.exercise == exercise
