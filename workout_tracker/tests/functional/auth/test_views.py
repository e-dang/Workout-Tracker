import pytest
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from tests.utils import invalidate_credentials

from users.models import User


@pytest.mark.django_db
def test_login(api_client, user_factory, test_password):
    url = reverse('rest_login')
    user = user_factory()

    resp = api_client.post(url, {'username': user.username, 'password': test_password})

    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert 'key' in resp.data
    assert len(resp.data['key']) == 40


@pytest.mark.django_db
def test_login_fail(api_client, user_factory, test_password):
    url = reverse('rest_login')
    user = user_factory()

    resp = api_client.post(url, {'email': user.email, 'password': test_password + 'wrong'})

    assert resp.status_code == 400


@pytest.mark.django_db
def test_logout(auto_login_user):
    url = reverse('rest_logout')
    api_client, _ = auto_login_user()

    resp = api_client.post(url)

    assert resp.status_code == 200
    assert len(Token.objects.all()) == 0


@pytest.mark.django_db
def test_logout_fail_invalid_credentials(auto_login_user):
    url = reverse('rest_logout')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)

    resp = api_client.post(url)

    assert resp.status_code == 401
    assert len(Token.objects.all()) == 1


@pytest.mark.django_db
def test_logout_fail_not_logged_in(auto_login_user):
    url = reverse('rest_logout')
    api_client, _ = auto_login_user()
    api_client.credentials()

    resp = api_client.post(url)

    assert resp.status_code == 200
    assert len(Token.objects.all()) == 1


@pytest.mark.parametrize('api_client, data', [
    (None, {'username': 'testname1', 'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe'}),
    (None, {'username': 'testname2', 'email': 'Johnoe@demo.com',
            'password1': 'thisisatest123', 'password2': 'thisisatest123'}),
],
    indirect=['api_client'],
    ids=['with_names', 'without_names'])
@pytest.mark.django_db
def test_registration(api_client, data):
    url = reverse('rest_register')
    before = len(User.objects.all())

    resp = api_client.post(url, data)

    assert resp.status_code == 201
    user = User.objects.get(email=data['email'])
    assert len(User.objects.all()) == before + 1
    assert resp.data['key'] == Token.objects.get(user=user.id).key


@pytest.mark.django_db
def test_rest_user_detail_get(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['username'] == user.username
    assert resp.data['email'] == user.email
    assert resp.data['first_name'] == user.first_name
    assert resp.data['last_name'] == user.last_name


@pytest.mark.django_db
def test_rest_user_detail_get_fail_invalid_credentials(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_rest_user_detail_get_fail_not_logged_in(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    api_client.credentials()

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_rest_user_detail_put(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()
    data = {'username': user.username, 'email': user.email,
            'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 200
    assert resp.data['username'] == data['username']
    assert resp.data['email'] == data['email']
    assert resp.data['first_name'] != user.first_name
    assert resp.data['last_name'] != user.last_name
    assert resp.data['first_name'] == data['first_name']
    assert resp.data['last_name'] == data['last_name']


@pytest.mark.django_db
def test_rest_user_detail_put_fail_invalid_credentials(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()
    invalidate_credentials(api_client)
    data = {'username': user.username, 'email': user.email,
            'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_rest_user_detail_put_fail_not_logged_in(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()
    api_client.credentials()
    data = {'username': user.username, 'email': user.email,
            'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 401
    assert resp.data['detail'].code == 'not_authenticated'


@pytest.mark.django_db
def test_rest_user_detail_put_fail_not_full_state(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 400


@pytest.mark.django_db
def test_rest_user_detail_patch(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.patch(url, data)

    assert resp.status_code == 200
    assert resp.data['username'] == user.username
    assert resp.data['email'] == user.email
    assert resp.data['first_name'] != user.first_name
    assert resp.data['last_name'] != user.last_name
    assert resp.data['first_name'] == data['first_name']
    assert resp.data['last_name'] == data['last_name']


@pytest.mark.django_db
def test_rest_user_detail_patch_fail_invalid_credentials(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.patch(url, data)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_rest_user_detail_patch_fail_not_logged_in(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    api_client.credentials()
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.patch(url, data)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_user_change_password(auto_login_user, test_password):
    url = reverse('rest_password_change')
    api_client, user = auto_login_user()
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password, 'old_password': test_password}

    resp = api_client.post(url, data)

    assert resp.status_code == 200
    assert User.objects.get(email=user.email).check_password(new_password)


@pytest.mark.django_db
def test_user_change_password_fail_invalid_credentials(auto_login_user, test_password):
    url = reverse('rest_password_change')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password, 'old_password': test_password}

    resp = api_client.post(url, data)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_user_change_password_fail_not_logged_in(auto_login_user, test_password):
    url = reverse('rest_password_change')
    api_client, _ = auto_login_user()
    api_client.credentials()
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password, 'old_password': test_password}

    resp = api_client.post(url, data)

    assert resp.status_code == 401


@pytest.mark.parametrize('auto_login_user, test_password, data, error_field', [
    (None, None, {'new_password2': 'a_different_test_password123', 'old_password': None}, 'new_password1'),
    (None, None, {'new_password1': 'a_unique_test_password123', 'old_password': None}, 'new_password2'),
    (None, None, {'new_password1': 'a_unique_test_password123',
                  'new_password2': 'a_unique_test_password123'}, 'old_password'),
    (None, None, {'new_password1': 'a_unique_test_password123',
                  'new_password2': 'a_different_test_password123', 'old_password': None}, 'new_password2'),
    (None, None, {'new_password1': 'a_unique_test_password123',
                  'new_password2': 'a_unique_test_password123', 'old_password': 'invalid_password'}, 'old_password')
],
    indirect=['auto_login_user', 'test_password'],
    ids=['missing new_password1', 'missing new_password2', 'missing old_password', 'mismatching new passwords', 'invalid old_password'])
@pytest.mark.django_db
def test_user_change_password_fail_invalid_input(auto_login_user, test_password, data, error_field):
    url = reverse('rest_password_change')
    api_client, _ = auto_login_user()
    if 'old_password' in data and data['old_password'] is None:
        data['old_password'] = test_password

    resp = api_client.post(url, data)

    assert resp.status_code == 400
    assert error_field in resp.data


@pytest.mark.parametrize('auto_login_user, logout', [
    (None, True),
    (None, False)
], indirect=['auto_login_user'], ids=['logged out', 'logged in'])
@pytest.mark.django_db
def test_password_reset_request(auto_login_user, logout):
    url = reverse('rest_password_reset')
    api_client, user = auto_login_user()
    if logout:
        api_client.credentials()

    resp = api_client.post(url, {'email': user.email})

    assert resp.status_code == 200
    assert resp.context['user'].email == user.email
    assert 'uid' in resp.context
    assert 'token' in resp.context


@pytest.mark.django_db
def test_password_reset_request_fail_invalid_credentials(auto_login_user):
    url = reverse('rest_password_reset')
    api_client, user = auto_login_user()
    invalidate_credentials(api_client)

    resp = api_client.post(url, {'email': user.email})

    assert resp.status_code == 401


@pytest.mark.parametrize('auto_login_user, logout', [
    (None, True),
    (None, False)
], indirect=['auto_login_user'], ids=['logged out', 'logged in'])
@pytest.mark.django_db
def test_password_reset_confirm(auto_login_user, logout):
    url = reverse('rest_password_reset')
    api_client, user = auto_login_user()
    if logout:
        api_client.credentials()
    resp = api_client.post(url, {'email': user.email})
    url = reverse('password_reset_confirm', kwargs={'token': resp.context['token'], 'uidb64': resp.context['uid']})
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password,
            'token': resp.context['token'], 'uid': resp.context['uid']}

    resp = api_client.post(url, data)

    assert resp.status_code == 200
    assert User.objects.get(email=user.email).check_password(new_password)


@pytest.mark.django_db
def test_password_reset_confirm_fail_invalid_credentials(auto_login_user):
    url = reverse('rest_password_reset')
    api_client, user = auto_login_user()
    resp = api_client.post(url, {'email': user.email})
    url = reverse('password_reset_confirm', kwargs={'token': resp.context['token'], 'uidb64': resp.context['uid']})
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password,
            'token': resp.context['token'], 'uid': resp.context['uid']}
    invalidate_credentials(api_client)

    resp = api_client.post(url, data)

    assert resp.status_code == 401


@pytest.mark.parametrize('auto_login_user, test_password, password1, password2, token, uid, error_field', [
    (None, None, 'thisisanewpassword123', 'thisisanewpassword', None, None, 'new_password2'),
    (None, None, 'thisisanewpassword123', 'thisisanewpassword123', 'WRONG_TOKEN', None, 'token'),
    (None, None, 'thisisanewpassword123', 'thisisanewpassword123', None, 'WRONG_UID', 'uid'),
],
    indirect=['auto_login_user', 'test_password'],
    ids=['mismatch passwords', 'wrong token', 'wrong uid'])
@pytest.mark.django_db
def test_password_reset_confirm_fail_invalid_input(auto_login_user, test_password, password1, password2, token, uid, error_field):
    url = reverse('rest_password_reset')
    api_client, user = auto_login_user()
    resp = api_client.post(url, {'email': user.email})
    url = reverse('password_reset_confirm', kwargs={'token': resp.context['token'], 'uidb64': resp.context['uid']})
    data = {'new_password1': password1, 'new_password2': password2,
            'token': token or resp.context['token'], 'uid': uid or resp.context['uid']}

    resp = api_client.post(url, data)

    assert resp.status_code == 400
    assert error_field in resp.data
    assert User.objects.get(email=user.email).check_password(test_password)
