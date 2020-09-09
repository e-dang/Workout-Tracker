from rest_framework.reverse import reverse

from tests.utils import add_api_prefix


def test_login_url():
    assert reverse('rest_login') == add_api_prefix('auth/login/')


def test_logout_url():
    assert reverse('rest_logout') == add_api_prefix('auth/logout/')


def test_user_registration_url():
    assert reverse('rest_register') == add_api_prefix('auth/register/')


def test_password_reset_url():
    assert reverse('rest_password_reset') == add_api_prefix('auth/password/reset/')


def test_password_reset_confirm_url():
    assert reverse('rest_password_reset_confirm') == add_api_prefix('auth/password/reset/confirm/')


def test_password_change_url():
    assert reverse('rest_password_change') == add_api_prefix('auth/password/change/')


def test_password_reset_confirm_with_tokens():
    uuid = 'uuid'
    token = 'reset-token'
    assert reverse('password_reset_confirm', kwargs={'uidb64': uuid,
                                                     'token': token}) == add_api_prefix(f'auth/password-reset-confirm/{uuid}/{token}/')
