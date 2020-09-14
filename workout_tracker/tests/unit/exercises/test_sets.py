import mock
import pytest

from exercises.models.sets import (KILOGRAMS, POUNDS, AbstractSet, Set,
                                   SetTemplate)


@pytest.mark.parametrize('old_data, new_data', [
    ({'reps': 10, 'weight': 100, 'units': KILOGRAMS, 'order': 0}, {'reps': 11, 'weight': 101, 'units': POUNDS}),
    ({'reps': 10, 'weight': 100, 'units': KILOGRAMS, 'order': 0}, {}),
],
    ids=['with_args', 'no_args'])
def test_abstract_set_update(old_data, new_data):
    mock_set = mock.MagicMock(spec=AbstractSet)
    mock_set.reps = old_data['reps']
    mock_set.weight = old_data['weight']
    mock_set.units = old_data['units']
    mock_set.order = old_data['order']

    AbstractSet.update(mock_set, **new_data)

    for key, value in new_data.items():
        if key != 'units':
            if value is not None:
                assert getattr(mock_set, key) == value
            else:
                assert getattr(mock_set, key) == old_data[key]
    unit_arg = new_data['units'] if 'units' in new_data else old_data['units']
    mock_set._change_units.assert_called_once_with(unit_arg)
    mock_set.save.assert_called_once()


@pytest.mark.parametrize('order, reps, weight, units, new_units, expected_util_call', [
    (0, 10, 100, KILOGRAMS, POUNDS, 'convert_kg_to_lb'),
    (0, 10, 100, POUNDS, KILOGRAMS, 'convert_lb_to_kg'),
    (0, 10, 100, KILOGRAMS, KILOGRAMS, None),
    (0, 10, 100, POUNDS, POUNDS, None),
],
    ids=['kg_to_lb', 'lb_to_kg', 'kg_to_kg', 'lb_to_lb'])
def test_abstract_set_change_units(order, reps, weight, units, new_units, expected_util_call):
    with mock.patch('exercises.models.sets.utils') as mock_utils:
        mock_set = mock.MagicMock(spec=AbstractSet)
        new_weight = 'new_weight'
        mock_set.order = order
        mock_set.reps = reps
        mock_set.weight = weight
        mock_set.units = units
        if expected_util_call is not None:
            getattr(mock_utils, expected_util_call).return_value = new_weight

        AbstractSet._change_units(mock_set, new_units)

        if units != new_units:
            assert mock_set.units == new_units
            assert mock_set.weight == new_weight
            getattr(mock_utils, expected_util_call).assert_called_once_with(weight)
        else:
            mock_utils.convert_lb_to_kg.assert_not_called()
            mock_utils.convert_kg_to_lb.assert_not_called()


def test_set_template_str():
    mock_set_template = mock.MagicMock(spec=SetTemplate)
    mock_set_template.reps = 10
    mock_set_template.weight = 100
    mock_set_template.units = KILOGRAMS

    ret_val = SetTemplate.__str__(mock_set_template)

    assert str(mock_set_template.reps) in ret_val
    assert str(mock_set_template.weight) in ret_val
    assert str(mock_set_template.units) in ret_val


def test_set_template_create_set():
    with mock.patch('exercises.models.sets.Set.from_template') as mock_constructor:
        mock_set_template = mock.MagicMock(spec=SetTemplate)
        mock_workload = mock.MagicMock()
        mock_set = mock.MagicMock()
        mock_constructor.return_value = mock_set

        ret_val = SetTemplate.create_set(mock_set_template, mock_workload)

        assert ret_val == mock_set
        mock_constructor.assert_called_once_with(mock_set_template, mock_workload)


def test_set_str():
    mock_set = mock.MagicMock(spec=Set)
    mock_set.reps = 10
    mock_set.weight = 100
    mock_set.units = KILOGRAMS
    mock_set.completed_reps = 9

    ret_val = Set.__str__(mock_set)

    assert str(mock_set.reps) in ret_val
    assert str(mock_set.weight) in ret_val
    assert str(mock_set.units) in ret_val
    assert str(mock_set.completed_reps) in ret_val


@pytest.mark.parametrize('set_factory, reps, completed_reps, expected', [
    (None, 10, 9, False),
    (None, 10, 10, True),
    (None, 10, 11, True),
],
    indirect=['set_factory'],
    ids=['less_than', 'equal', 'greater_than'])
def test_set_is_complete(set_factory, reps, completed_reps, expected):
    _set = set_factory.build(reps=reps, completed_reps=completed_reps)

    assert _set.is_complete == expected


def test_set_from_template(set_factory, set_template_factory, workload_factory):
    with mock.patch('exercises.models.sets.Set.objects') as mock_manager:
        set_template = set_template_factory.build()
        workload = workload_factory.build()
        kwargs = {'order': set_template.order, 'units': set_template.units, 'weight': set_template.weight,
                  'reps': set_template.reps, 'workload': workload, 'completed_reps': 0}
        _set = set_factory.build(**kwargs)
        mock_manager.create.return_value = _set

        ret_val = Set.from_template(set_template, workload)

        assert ret_val == _set
        mock_manager.create.assert_called_once_with(**kwargs)
