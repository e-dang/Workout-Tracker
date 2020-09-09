import pytest
import mock

from muscles.models import Muscle, MuscleGrouping
from muscles import utils


@pytest.fixture(autouse=True)
def mock_logger():
    with mock.patch('muscles.utils.logging') as mock_logging:
        _mock_logger = mock.MagicMock()
        mock_logging.getLogger.return_value = _mock_logger
        yield _mock_logger


def test_percolate_created():
    mock_instance = mock.MagicMock(spec=Muscle)
    mock_model = mock.MagicMock(spec=Muscle)
    mock_next_level_instance = mock.MagicMock(spec=MuscleGrouping)
    related_name = 'muscles'
    mock_instance.name = 'test_name'
    mock_instance.snames = ['test_name1', 'test_name2']
    mock_model.objects.create.return_value = mock_next_level_instance

    utils.percolate(mock_instance, True, mock_model, related_name)

    mock_model.objects.create.assert_called_once_with(name=mock_instance.name, snames=mock_instance.snames)
    getattr(mock_next_level_instance, related_name).add.assert_called_once_with(mock_instance)


def test_percolate_not_created():
    mock_instance = mock.MagicMock(spec=Muscle)
    mock_model = mock.MagicMock(spec=Muscle)
    mock_next_level_instance = mock.MagicMock(spec=MuscleGrouping)
    related_name = 'muscles'
    mock_instance.name = 'test_name'
    mock_instance.snames = ['test_name1', 'test_name2']
    mock_model.objects.create.return_value = mock_next_level_instance

    utils.percolate(mock_instance, False, mock_model, related_name)

    mock_model.objects.create.assert_not_called()
    getattr(mock_next_level_instance, related_name).add.assert_not_called()
    mock_next_level_instance.delete.assert_not_called()


def test_percolate_created_attr_err():
    mock_instance = mock.MagicMock(spec=Muscle)
    mock_model = mock.MagicMock(spec=Muscle)
    mock_next_level_instance = mock.Mock(spec=MuscleGrouping)
    related_name = 'muscle'
    mock_instance.name = 'test_name'
    mock_instance.snames = ['test_name1', 'test_name2']
    mock_model.objects.create.return_value = mock_next_level_instance

    utils.percolate(mock_instance, True, mock_model, related_name)

    mock_model.objects.create.assert_called_once_with(name=mock_instance.name, snames=mock_instance.snames)
    mock_next_level_instance.delete.assert_called_once()


def test_enforce_no_empty_relationships():
    mock_instance = mock.Mock(spec=Muscle)
    related_name = 'groupings'
    reverse_related_name = 'muscles'
    groupings = [mock.Mock(spec=MuscleGrouping) for _ in range(2)]
    groupings[0].muscles = mock.MagicMock(**{'all.return_value': mock.MagicMock(**{'count.return_value': 1})})
    groupings[1].muscles = mock.MagicMock(**{'all.return_value': mock.MagicMock(**{'count.return_value': 2})})
    mock_instance.groupings.all.return_value = groupings

    utils.enforce_no_empty_relationships(mock_instance, related_name, reverse_related_name)

    groupings[0].delete.assert_called_once()


def test_enforce_no_empty_relationships_fail_wrong_related_name():
    mock_instance = mock.Mock(spec=Muscle)
    wrong_related_name = 'grouping'
    reverse_related_name = 'muscles'
    groupings = [mock.Mock(spec=MuscleGrouping) for _ in range(2)]
    groupings[0].muscles = mock.MagicMock(**{'all.return_value': mock.MagicMock(**{'count.return_value': 1})})
    groupings[1].muscles = mock.MagicMock(**{'all.return_value': mock.MagicMock(**{'count.return_value': 2})})
    mock_instance.groupings.all.return_value = groupings

    utils.enforce_no_empty_relationships(mock_instance, wrong_related_name, reverse_related_name)

    mock_instance.groupings.all.assert_not_called()
    groupings[0].delete.assert_not_called()
    groupings[1].delete.assert_not_called()


def test_enforce_no_empty_relationships_fail_attr_err():
    mock_instance = mock.Mock(spec=Muscle)
    related_name = 'groupings'
    wrong_reverse_related_name = 'muscle'
    groupings = [mock.Mock(spec=MuscleGrouping) for _ in range(2)]
    groupings[0].muscles = mock.MagicMock(**{'all.return_value': mock.MagicMock(**{'count.return_value': 1})})
    groupings[1].muscles = mock.MagicMock(**{'all.return_value': mock.MagicMock(**{'count.return_value': 2})})
    mock_instance.groupings.all.return_value = groupings

    utils.enforce_no_empty_relationships(mock_instance, related_name, wrong_reverse_related_name)

    groupings[0].delete.assert_not_called()
    groupings[1].delete.assert_not_called()
