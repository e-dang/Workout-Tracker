import pytest

from equipment.models import Equipment
from exercises.models import (Exercise, ExerciseTemplate, Set,
                              SetTemplate, Workload, WorkloadTemplate)
from movements.models import Movement
from muscles.models import Muscle, MuscleGrouping, MuscleSubportion
from users.models import User


@pytest.mark.django_db
def test_user_factory(user_factory):
    user = user_factory()

    assert isinstance(user, User)


@pytest.mark.django_db
def test_muscle_subportion_factory(muscle_subportion_factory):
    grouping = muscle_subportion_factory()

    assert isinstance(grouping, MuscleSubportion)
    assert MuscleSubportion.objects.all().count() == 1
    assert Muscle.objects.all().count() == 1
    assert MuscleGrouping.objects.all().count() == 1


@pytest.mark.parametrize('muscle_factory, num_subportions, expected_grouping, expected_muscle, expected_subportion', [
    (None, 0, 1, 1, 0),
    (None, 1, 2, 2, 1),
    (None, 2, 3, 3, 2)
], indirect=['muscle_factory'])
@pytest.mark.django_db
def test_muscle_factory(muscle_factory, num_subportions, expected_grouping, expected_muscle, expected_subportion):
    muscle = muscle_factory(subportions=num_subportions)

    assert isinstance(muscle, Muscle)
    assert muscle.subportions.all().count() == num_subportions
    assert Muscle.objects.all().count() == expected_muscle
    assert MuscleGrouping.objects.all().count() == expected_grouping
    assert MuscleSubportion.objects.all().count() == expected_subportion


@pytest.mark.parametrize('muscle_grouping_factory, num_muscles, expected_grouping, expected_muscle, expected_subportion', [
    (None, 0, 1, 0, 0),
    (None, 1, 3, 2, 1),
    (None, 2, 5, 4, 2)
], indirect=['muscle_grouping_factory'])
@pytest.mark.django_db
def test_muscle_grouping_factory(muscle_grouping_factory, num_muscles, expected_grouping, expected_muscle, expected_subportion):
    grouping = muscle_grouping_factory(muscles=num_muscles)

    assert isinstance(grouping, MuscleGrouping)
    assert grouping.muscles.all().count() == num_muscles
    assert MuscleGrouping.objects.all().count() == expected_grouping
    assert Muscle.objects.all().count() == expected_muscle
    assert MuscleSubportion.objects.all().count() == expected_subportion


@pytest.mark.django_db
def test_equipment_factory(equipment_factory):
    equipment = equipment_factory()

    assert isinstance(equipment, Equipment)
    assert isinstance(equipment.owner, User)


@pytest.mark.django_db
def test_user_factory_with_equipment(user_factory):
    num_equipment = 5
    user = user_factory(equipment=num_equipment)

    user_equipment = user.equipments.all()
    assert user_equipment.count() == num_equipment
    for equipment in user_equipment:
        assert equipment.owner == user


@pytest.mark.parametrize('num_equipment', [
    0,
    1,
    2
],
    ids=['zero_equipment', 'one_equipment', 'two_equipment'])
@pytest.mark.parametrize('num_muscles', [
    0,
    1,
    2
],
    ids=['zero_muscles', 'one_muscles', 'two_muscles'])
@pytest.mark.parametrize('movement_factory', [
    None
],
    indirect=['movement_factory'],
    ids=[''])
@pytest.mark.django_db
def test_movement_factory(movement_factory, num_muscles, num_equipment):
    movement = movement_factory(muscles=num_muscles, equipment=num_equipment)

    muscles_count = movement.muscles.all().count()
    equipment_count = movement.equipment.all().count()
    assert isinstance(movement, Movement)
    assert isinstance(movement.owner, User)
    assert muscles_count == num_muscles
    assert equipment_count == num_equipment
    if muscles_count != 0:
        assert isinstance(movement.muscles.last(), MuscleGrouping)
    if equipment_count != 0:
        assert isinstance(movement.equipment.last(), Equipment)


@pytest.mark.django_db
def test_user_factory_with_movements(user_factory):
    num_movements = 5
    user = user_factory(movements=num_movements)

    user_movements = user.movements.all()
    assert user_movements.count() == num_movements
    for movement in user_movements:
        assert movement.owner == user


@pytest.mark.django_db
def test_set_template_factory(set_template_factory):
    set_template = set_template_factory()

    assert isinstance(set_template, SetTemplate)
    assert isinstance(set_template.workload_template, WorkloadTemplate)


@pytest.mark.django_db
def test_set_factory(set_factory):
    set = set_factory()

    assert isinstance(set, Set)
    assert isinstance(set.workload, Workload)


@pytest.mark.django_db
def test_workload_template_factory(workload_template_factory):
    workload_template = workload_template_factory()

    assert isinstance(workload_template, WorkloadTemplate)
    assert isinstance(workload_template.exercise_template, ExerciseTemplate)


@pytest.mark.django_db
def test_workload_factory(workload_factory):
    workload = workload_factory()

    assert isinstance(workload, Workload)
    assert isinstance(workload.exercise, Exercise)


@pytest.mark.django_db
def test_exercise_template_factory(exercise_template_factory):
    exercise_template = exercise_template_factory()

    assert isinstance(exercise_template, ExerciseTemplate)


@pytest.mark.django_db
def test_exercise_factory(exercise_factory):
    exercise = exercise_factory()

    assert isinstance(exercise, Exercise)


@pytest.mark.parametrize('factory, workload_class, set_class', [
    (pytest.lazy_fixture('workload_template_factory'), WorkloadTemplate, SetTemplate),
    (pytest.lazy_fixture('workload_factory'), Workload, Set)
],
    ids=['workload_template', 'workload'])
@pytest.mark.parametrize('num_sets', [
    0,
    1
],
    ids=['zero_sets', 'one_set'])
@pytest.mark.django_db
def test_workload_factory_with_sets(factory, workload_class, set_class, num_sets):
    workload = factory(sets=num_sets)

    sets = workload.sets.all()
    assert isinstance(workload, workload_class)
    assert isinstance(workload.movement, Movement)
    assert sets.count() == num_sets
    if sets.count() != 0:
        assert isinstance(sets[0], set_class)


@pytest.mark.parametrize('factory, exercise_class, workload_class, set_class', [
    (pytest.lazy_fixture('exercise_template_factory'), ExerciseTemplate, WorkloadTemplate, SetTemplate),
    (pytest.lazy_fixture('exercise_factory'), Exercise, Workload, Set)
],
    ids=['workload_template', 'workload'])
@pytest.mark.parametrize('num_workloads, num_sets', [
    (0, 0),
    (0, 2),
    (2, 0),
    (2, 3)
],
    ids=['0_workloads_0_sets', '2_sets', '2_workloads', '2_workloads_3_sets'])
@pytest.mark.django_db
def test_exercises_with_workloads(factory, exercise_class, workload_class, set_class, num_workloads, num_sets):
    exercise = factory(workloads=num_workloads, workloads__sets=num_sets)

    workloads = exercise.workloads.all()
    assert isinstance(exercise, exercise_class)
    assert workloads.count() == num_workloads
    for workload in workloads:
        assert isinstance(workload, workload_class)
        set = workload.sets.all()
        assert set.count() == num_sets
        if set.count() != 0:
            assert isinstance(set[0], set_class)
