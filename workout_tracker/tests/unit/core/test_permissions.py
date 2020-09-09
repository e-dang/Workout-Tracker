import mock
import pytest

from core.permissions import IsAdmin, IsOwner


@pytest.mark.parametrize('user_factory, is_user', [
    (None, False),
    (None, True)
],
    indirect=['user_factory'],
    ids=['obj_isnt_user', 'obj_is_user'])
def test_is_owner_has_object_permission(user_factory, is_user):
    user = user_factory.build()
    mock_request = mock.MagicMock()
    permission = IsOwner()
    mock_request.user = user
    if is_user:
        obj = user
    else:
        obj = mock.MagicMock()
        obj.owner = user

    assert permission.has_object_permission(mock_request, mock.MagicMock(), obj)


@pytest.mark.parametrize('user_factory, is_user', [
    (None, False),
    (None, True)
],
    indirect=['user_factory'],
    ids=['obj_isnt_user', 'obj_is_user'])
def test_is_owner_has_object_permission_fail(user_factory, is_user):
    user1 = user_factory.build()
    user2 = user_factory.build()
    mock_request = mock.MagicMock()
    permission = IsOwner()
    mock_request.user = user1
    if is_user:
        obj = user2
    else:
        obj = mock.MagicMock()
        obj.owner = user2

    assert not permission.has_object_permission(mock_request, mock.MagicMock(), obj)


@pytest.mark.parametrize('user_factory, use_pk', [
    (None, True),
    (None, False)
], indirect=['user_factory'],
    ids=['pk', 'no_pk'])
@pytest.mark.parametrize('is_authenticated, expected', [
    (True, True),
    (False, False)
],
    ids=['is_authenticated', 'is_not_authenticated'])
def test_is_owner_has_permission(user_factory, use_pk, is_authenticated, expected):
    user = user_factory.build()
    mock_request = mock.MagicMock()
    mock_view = mock.MagicMock()
    permission = IsOwner()

    mock_request.user.is_authenticated = is_authenticated
    mock_request.user.pk = user.pk
    if use_pk:
        mock_view.kwargs = {'pk': user.pk}
    else:
        mock_view.kwargs = {}

    assert expected == permission.has_permission(mock_request, mock_view)


@pytest.mark.parametrize('user_factory, use_pk', [
    (None, True),
    (None, False)
], indirect=['user_factory'],
    ids=['pk', 'no_pk'])
@pytest.mark.parametrize('is_authenticated, expected', [
    (True, True),
    (False, False)
],
    ids=['is_authenticated', 'is_not_authenticated'])
def test_is_owner_has_permission_different_pk(user_factory, use_pk, is_authenticated, expected):
    user = user_factory.build()
    mock_request = mock.MagicMock()
    mock_view = mock.MagicMock()
    permission = IsOwner()

    mock_request.user.is_authenticated = is_authenticated
    mock_request.user.pk = user.pk
    if use_pk:
        mock_view.kwargs = {'pk': '-1'}
        expected = False
    else:
        mock_view.kwargs = {}

    assert expected == permission.has_permission(mock_request, mock_view)


@pytest.mark.parametrize('is_admin', [
    True,
    False
],
    ids=['is_admin', 'is_not_admin'])
def test_is_admin_has_object_permission(is_admin):
    mock_request = mock.MagicMock()
    mock_view = mock.MagicMock()
    mock_object = mock.MagicMock()
    permissions = IsAdmin()

    mock_request.user.is_staff = is_admin

    assert permissions.has_object_permission(mock_request, mock_view, mock_object) is is_admin
