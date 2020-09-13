import pytest
from exercises.models import ExerciseTemplate, Exercise, WorkloadTemplate, Workload, SetTemplate, Set


@pytest.mark.parametrize('exercise_template_factory, num_workloads, num_sets', [
    (None, 0, 0),
    (None, 1, 0),
    (None, 1, 3),
    (None, 2, 3)
],
    indirect=['exercise_template_factory'],
    ids=['0_workloads_0_sets', '1_workloads_0_sets', '1_workloads_3_sets', '2_workloads_3_sets'])
@pytest.mark.django_db
def test_create_exercise(exercise_template_factory, num_workloads, num_sets):
    exercise_template = exercise_template_factory(workloads=num_workloads, workloads__sets=num_sets)

    exercise = exercise_template.create_exercise()

    assert isinstance(exercise, Exercise)
    workloads = exercise.workloads.all()
    assert workloads.count() == num_workloads
    for workload in workloads:
        assert isinstance(workload, Workload)
        sets = workload.sets.all()
        assert sets.count() == num_sets
        if num_sets != 0:
            assert isinstance(sets[0], Set)
