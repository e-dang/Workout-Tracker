import pytest


def _get_test_type(item):
    return item.nodeid.split('/')[1]


def pytest_collection_modifyitems(items):
    for item in items:
        test_type = _get_test_type(item)
        if test_type == 'unit':
            item.add_marker(pytest.mark.unit)
        elif test_type == 'functional':
            item.add_marker(pytest.mark.functional)
        elif test_type == 'integration':
            item.add_marker(pytest.mark.integration)
