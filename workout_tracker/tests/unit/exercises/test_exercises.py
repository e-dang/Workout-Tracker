import pytest
import mock

from tests.factories import SetFactory
from exercises.models import Workload, WorkloadTemplate, KILOGRAMS
from exercises.models.exercises import AbstractExercise


@pytest.fixture
def mock_abstract_exercise():
    yield mock.MagicMock(spec=AbstractExercise, workloads=mock.MagicMock())


class TestAbstractExercise:
    def test_getitem(self, mock_abstract_exercise):
        target_ret_val = 3
        arg = 1
        mock_abstract_exercise.get.return_value = target_ret_val

        ret_val = AbstractExercise.__getitem__(mock_abstract_exercise, arg)

        assert ret_val == target_ret_val

    def test_getitem_fail(self, mock_abstract_exercise):
        target_ret_val = None
        arg = 1
        mock_abstract_exercise.get.return_value = target_ret_val

        with pytest.raises(KeyError):
            _ = AbstractExercise.__getitem__(mock_abstract_exercise, arg)

    def test_repr(self, workload_factory, mock_abstract_exercise):
        test_name = 'test'
        workloads = workload_factory.build_batch(3)
        mock_abstract_exercise.workloads.all.return_value = workloads
        mock_abstract_exercise.__str__.return_value = test_name

        ret_val = AbstractExercise.__repr__(mock_abstract_exercise)

        assert test_name in ret_val
        for workload in workloads:
            assert str(workload) in ret_val

    def test_len(self, mock_abstract_exercise):
        length = 3
        mock_abstract_exercise.workloads.all().count.return_value = length

        ret_val = AbstractExercise.__len__(mock_abstract_exercise)

        assert ret_val == length

    def test_get(self, mock_abstract_exercise):
        call_arg = 3
        return_value = 1
        mock_abstract_exercise.workloads.get.return_value = return_value

        ret_val = AbstractExercise.get(mock_abstract_exercise, call_arg)

        assert ret_val == return_value
        mock_abstract_exercise.workloads.get.assert_called_once_with(order=call_arg)

    @pytest.mark.parametrize('mock_abstract_exercise, side_effect', [
        (None, Workload.DoesNotExist),
        (None, WorkloadTemplate.DoesNotExist)
    ],
        indirect=['mock_abstract_exercise'])
    @pytest.mark.parametrize('default', [
        None,
        2
    ])
    def test_get_default(self, mock_abstract_exercise, side_effect, default):
        call_arg = 3
        mock_abstract_exercise.workloads.get.side_effect = side_effect

        ret_value = AbstractExercise.get(mock_abstract_exercise, call_arg, default=default)

        assert ret_value == default
        mock_abstract_exercise.workloads.get.assert_called_once_with(order=call_arg)

    @pytest.mark.parametrize('mock_abstract_exercise, movement_factory, units, order, num_workloads, set_factory', [
        (None, None, KILOGRAMS, None, 0, None),
        (None, None, KILOGRAMS, 0, 0, None),
        (None, None, KILOGRAMS, 1, 1, None)
    ],
        indirect=['mock_abstract_exercise', 'movement_factory', 'set_factory'],
        ids=['order_not_given', 'order=0', 'order=1'])
    def test_append(self, mock_abstract_exercise, movement_factory, units, order, num_workloads, set_factory):
        mock_abstract_exercise.__len__.return_value = num_workloads
        movement = movement_factory.build()
        sets = set_factory.json(reps=12)

        AbstractExercise.append(
            mock_abstract_exercise,
            movement,
            units,
            order=order,
            sets=sets
        )

        called_order = order or num_workloads
        mock_abstract_exercise.workloads.create.assert_called_once_with(
            movement=movement, units=units, order=called_order, sets=sets)
        if order is None or order == 0:
            mock_abstract_exercise.__len__.assert_called_once()
        else:
            mock_abstract_exercise.__len__.assert_not_called()

    def test_extend(self, mock_abstract_exercise, workload_factory):
        workloads = workload_factory.json_batch(3)
        AbstractExercise.extend(mock_abstract_exercise, workloads)

        calls = [mock.call(**workload) for workload in workloads]
        mock_abstract_exercise.append.assert_has_calls(calls)

    def test_remove(self, mock_abstract_exercise):
        idx = 1
        AbstractExercise.remove(mock_abstract_exercise, idx)

        mock_abstract_exercise.__delitem__.assert_called_once_with(idx)


class TestExerciseTemplate:
    def test_create_exercise(self, exercise_template_factory, exercise_factory):
        with mock.patch('exercises.models.exercises.Exercise') as mock_exercise_class:
            exercise_template = exercise_template_factory.build()
            exercise = exercise_factory.build()
            mock_exercise_class.from_template.return_value = exercise

            ret_val = exercise_template.create_exercise()

            assert ret_val == exercise
            mock_exercise_class.from_template.assert_called_once_with(exercise_template)


class TestExercise:
    @pytest.mark.parametrize('exercise_factory, workload1_state, workload2_state, expected', [
        (None, False, False, False),
        (None, False, True, False),
        (None, True, True, True)
    ],
        indirect=['exercise_factory'],
        ids=['both_incomplete', '1_incomplete_1_complete', 'both_complete'])
    def test_is_complete(self, exercise_factory, workload1_state, workload2_state, expected):
        with mock.patch('exercises.models.exercises.Exercise.workloads') as mock_manager:
            mock_workloads = [mock.MagicMock(spec=Workload) for _ in range(2)]
            mock_workloads[0].is_complete = workload1_state
            mock_workloads[1].is_complete = workload2_state
            mock_manager.all.return_value = mock_workloads
            exercise = exercise_factory.build()

            assert exercise.is_complete == expected
