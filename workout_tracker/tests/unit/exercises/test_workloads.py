import pytest
import mock

from exercises.models.workloads import AbstractWorkload, WorkloadTemplate, Workload, KILOGRAMS, POUNDS
from exercises.models.sets import AbstractSet, Set, SetTemplate


def test_abstract_workload_str(set_factory, movement_factory):
    sets = set_factory.build_batch(3)
    movement = movement_factory.build()
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.movement = movement
    mock_workload.sets = mock.MagicMock()
    mock_workload.sets.all.return_value = sets

    ret_val = AbstractWorkload.__str__(mock_workload)

    assert str(movement) in ret_val
    for s in sets:
        assert str(s) in ret_val


def test_abstract_workload_getitem():
    arg = 1
    gotten_item = 5
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.get.return_value = gotten_item

    ret_val = AbstractWorkload.__getitem__(mock_workload, arg)

    assert ret_val == 5
    mock_workload.get.assert_called_once_with(arg)


def test_abstract_workload_getitem_fail():
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.get.return_value = None

    with pytest.raises(KeyError):
        _ = AbstractWorkload.__getitem__(mock_workload, 1)


def test_abstract_workload_len():
    length = 2
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.sets = mock.MagicMock()
    mock_workload.sets.all().count.return_value = length

    ret_val = AbstractWorkload.__len__(mock_workload)

    assert ret_val == length


def test_abstract_workload_get():
    idx = 3
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.sets = mock.MagicMock()
    mock_workload.sets.get.side_effect = lambda order=None: list(range(5))[order]

    ret_val = AbstractWorkload.get(mock_workload, idx)

    assert ret_val == idx


@pytest.mark.parametrize('side_effect', [
    Set.DoesNotExist,
    SetTemplate.DoesNotExist
],
    ids=['set', 'set_template'])
@pytest.mark.parametrize('default', [
    None,
    1
],
    ids=['None', '1'])
def test_abstract_workload_get_default(side_effect, default):
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.sets = mock.MagicMock()
    mock_workload.sets.get.side_effect = side_effect

    ret_val = AbstractWorkload.get(mock_workload, 1, default=default)

    assert ret_val == default


@pytest.mark.parametrize('factory, units, new_movement, new_units', [
    (pytest.lazy_fixture('movement_factory'), KILOGRAMS, True, POUNDS),
    (pytest.lazy_fixture('movement_factory'), KILOGRAMS, None, None)
])
def test_abstract_workload_update(factory, units, new_movement, new_units):
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    movement = factory.build()
    mock_workload.movement = movement
    mock_workload.units = units
    if new_movement:
        new_movement = factory.build()

    AbstractWorkload.update(mock_workload, movement=new_movement, units=new_units)

    called_units = new_units or units
    mock_workload._change_units.assert_called_once_with(called_units)
    mock_workload.movement = new_movement or movement
    if new_movement is None and new_units is None:
        mock_workload.save.assert_not_called()
    else:
        mock_workload.save.assert_called_once()


@pytest.mark.parametrize('reps, weight, units, order', [
    (10, 100, KILOGRAMS, 0),
    (10, 100, None, None)
])
def test_abstract_workload_append(reps, weight, units, order):
    length = 2
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_set = mock.MagicMock(spec=AbstractSet)
    mock_set.units = units
    mock_workload.units = units
    mock_workload._build_set.return_value = mock_set
    mock_workload.__len__.return_value = length

    AbstractWorkload.append(mock_workload, reps, weight, units=units, order=order)

    mock_workload._build_set.assert_called_once_with(reps, weight, units or mock_workload.units, order or length)
    mock_set._change_units.assert_called_once_with(mock_workload.units)
    mock_set.save.assert_called_once()


def test_abstract_workload_extend():
    sets = [{'reps': 10, 'weights': 100}, {'reps': 11, 'weights': 101}]
    mock_workload = mock.MagicMock(spec=AbstractWorkload)

    AbstractWorkload.extend(mock_workload, sets)

    mock_workload.append.assert_has_calls([mock.call(**s) for s in sets])


@pytest.mark.parametrize('sets', [
    None,
    ['not mapping']
],
    ids=['not_iterable', 'not_mapping'])
def test_abstract_workload_extend_fail(sets):
    mock_workload = mock.MagicMock(spec=AbstractWorkload)

    with pytest.raises(TypeError):
        AbstractWorkload.extend(mock_workload, sets)


def test_abstract_workload_remove():
    idx = 1
    mock_workload = mock.MagicMock(spec=AbstractWorkload)

    AbstractWorkload.remove(mock_workload, idx)

    mock_workload.__delitem__.assert_called_once_with(idx)


@pytest.mark.parametrize('old_units, new_units', [
    (KILOGRAMS, POUNDS),
    (POUNDS, KILOGRAMS),
    (KILOGRAMS, KILOGRAMS),
    (POUNDS, POUNDS)
])
def test_abstract_workload_change_units(old_units, new_units):
    mock_workload = mock.MagicMock(spec=AbstractWorkload)
    mock_workload.units = old_units
    mock_workload.sets = mock.MagicMock()
    sets = [mock.MagicMock(spec=AbstractSet, units=old_units) for _ in range(3)]
    mock_workload.sets.all.return_value = sets

    AbstractWorkload._change_units(mock_workload, new_units)

    mock_workload.units == new_units
    if old_units != new_units:
        for s in sets:
            s._change_units.assert_called_once_with(new_units)
    else:
        for s in sets:
            s._change_units.assert_not_called()


def test_abstract_workload_build_set():
    with pytest.raises(NotImplementedError):
        AbstractWorkload._build_set(mock.MagicMock(spec=AbstractWorkload), 10, 100, KILOGRAMS, 0)


def test_workload_template_create_workload(workload_template_factory, exercise_factory, workload_factory):
    with mock.patch('exercises.models.workloads.Workload.from_template') as mock_constructor:
        workload_template = workload_template_factory.build()
        exercise = exercise_factory.build()
        kwargs = {'order': workload_template.order, 'units': workload_template.units,
                  'movement': workload_template.movement, 'exercise': exercise}
        workload = workload_factory.build(**kwargs)
        mock_constructor.return_value = workload

        ret_val = workload_template.create_workload(exercise)

        assert ret_val is workload
        mock_constructor.assert_called_once_with(workload_template, exercise)


@pytest.mark.parametrize('factory, set_type', [
    (pytest.lazy_fixture('workload_template_factory'), SetTemplate),
    (pytest.lazy_fixture('workload_factory'), Set)
],
    ids=['workload_template', 'workload'])
def test_workload_build_set(factory, set_type):
    workload = factory.build()
    reps = 10
    weight = 100
    units = KILOGRAMS
    order = 0

    s = workload._build_set(reps, weight, units, order)

    assert isinstance(s, set_type)
    assert s.reps == reps
    assert s.weight == weight
    assert s.units == units
    assert s.order == order
