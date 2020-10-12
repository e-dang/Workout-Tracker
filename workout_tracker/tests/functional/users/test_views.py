import pytest
from rest_framework.reverse import reverse

from users.models import User
from users.serializers import UserSerializer
from tests.utils import get_resp_data


@pytest.mark.parametrize('get_client_user, status_code', [
    (pytest.lazy_fixture('client_logged_in_active_user'), 200),
    (pytest.lazy_fixture('client_logged_in_inactive_user'), 401),
    (pytest.lazy_fixture('client_logged_in_admin_user'), 200),
    (pytest.lazy_fixture('client_logged_in_superuser'), 200),
    (pytest.lazy_fixture('client_logged_out_user'), 401)
],
    ids=['active', 'inactive', 'admin', 'superuser', 'logged_out'])
@pytest.mark.django_db
def test_user_list(get_client_user, status_code):
    api_client, _ = get_client_user(num_add_users=2)
    url = reverse('user-list')

    resp = api_client.get(url)

    assert resp.status_code == status_code
    if status_code == 200:
        data = get_resp_data(resp)
        assert len(data) == User.objects.all().count()
        assert len(UserSerializer.Meta.fields) == len(data[0])
        for field in UserSerializer.Meta.fields:
            assert field in data[0]


@pytest.mark.parametrize('get_client_user, status_code', [
    (pytest.lazy_fixture('client_logged_in_active_user'), 200),
    (pytest.lazy_fixture('client_logged_in_inactive_user'), 401),
    (pytest.lazy_fixture('client_logged_in_admin_user'), 200),
    (pytest.lazy_fixture('client_logged_in_superuser'), 200),
    (pytest.lazy_fixture('client_logged_out_user'), 401)
],
    ids=['active', 'inactive', 'admin', 'superuser', 'logged_out'])
@pytest.mark.django_db
def test_user_detail(get_client_user, status_code):
    api_client, user = get_client_user()
    url = reverse('user-detail', kwargs={'pk': user.pk})

    resp = api_client.get(url)

    assert resp.status_code == status_code
    if status_code == 200:
        assert len(UserSerializer.Meta.fields) == len(resp.data)
        for field in UserSerializer.Meta.fields:
            if hasattr(user, field):
                assert resp.data[field] == getattr(user, field)


@pytest.mark.parametrize('get_client_user, status_code, is_active', [
    (pytest.lazy_fixture('client_logged_in_active_user'), 204, False),
    (pytest.lazy_fixture('client_logged_in_inactive_user'), 401, False),
    (pytest.lazy_fixture('client_logged_in_admin_user'), 204, False),
    (pytest.lazy_fixture('client_logged_in_superuser'), 204, False),
    (pytest.lazy_fixture('client_logged_out_user'), 401, True)
],
    ids=['active', 'inactive', 'admin', 'superuser', 'logged_out'])
@pytest.mark.django_db
def test_user_detail_delete(get_client_user, status_code, is_active):
    api_client, user = get_client_user()
    pk = user.pk
    url = reverse('user-detail', kwargs={'pk': pk})
    before = len(User.objects.all())

    resp = api_client.delete(url)

    assert resp.status_code == status_code
    assert len(User.objects.all()) == before
    assert User.objects.get(pk=pk).is_active == is_active
