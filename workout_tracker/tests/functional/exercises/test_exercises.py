import pytest

from exercises.models import Exercise, Set, Workload


@pytest.fixture(autouse=True)
def reset_workload_sequence(workload_factory, workload_template_factory):
    workload_factory.reset_sequence(0)
    workload_template_factory.reset_sequence(0)
    yield


@pytest.mark.parametrize('factory, num_workloads, idx', [
    (pytest.lazy_fixture('exercise_factory'), 2, 1),
    (pytest.lazy_fixture('exercise_template_factory'), 2, 1)
],
    ids=['exercise', 'exercise_template'])
@pytest.mark.django_db
def test_exercise_delitem(factory, num_workloads, idx):
    exercise = factory(workloads=num_workloads)

    del exercise[idx]

    workloads = exercise.workloads.all()
    assert workloads.count() == num_workloads - 1
    assert [workload.order for workload in workloads] == list(range(num_workloads - 1))


@pytest.mark.parametrize('factory, num_workloads, idx1, idx2', [
    (pytest.lazy_fixture('exercise_factory'), 3, 0, 2),
    (pytest.lazy_fixture('exercise_template_factory'), 3, 0, 2)
],
    ids=['exercise', 'exercise_template'])
@pytest.mark.django_db
def test_exercise_swap_workloads(factory, num_workloads, idx1, idx2):
    exercise = factory(workloads=num_workloads)
    workloads = exercise.workloads.all()
    workload1 = workloads[idx1]
    workload2 = workloads[idx2]

    exercise.swap_workloads(idx1, idx2)

    workloads = exercise.workloads.all()
    assert workloads[idx1] == workload2
    assert workloads[idx2] == workload1


@pytest.mark.parametrize('exercise_template_factory, num_workloads, num_sets', [
    (None, 0, 0),
    (None, 1, 0),
    (None, 1, 3),
    (None, 2, 3)
],
    indirect=['exercise_template_factory'],
    ids=['0_workloads_0_sets', '1_workloads_0_sets', '1_workloads_3_sets', '2_workloads_3_sets'])
@pytest.mark.django_db
def test_exercise_from_template(exercise_template_factory, num_workloads, num_sets):
    exercise_template = exercise_template_factory(workloads=num_workloads, workloads__sets=num_sets)

    exercise = Exercise.from_template(exercise_template)

    assert isinstance(exercise, Exercise)
    workloads = exercise.workloads.all()
    assert workloads.count() == num_workloads
    for workload in workloads:
        assert isinstance(workload, Workload)
        sets = workload.sets.all()
        assert sets.count() == num_sets
        if num_sets != 0:
            assert isinstance(sets[0], Set)
