import pytest

import factory

from users.models import User

TEST_PASSWORD = 'strong-test-pass123'


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda x: f'username{x}')
    email = factory.Faker('email')
    password = TEST_PASSWORD
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = 'users.User'

    class Params:
        inactive = factory.Trait(
            is_active=False,
            is_staff=False,
            is_superuser=False
        )
        active = factory.Trait(
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        admin = factory.Trait(
            is_active=True,
            is_staff=True,
            is_superuser=False
        )
        superuser = factory.Trait(
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


@pytest.mark.django_db
def test_user_factory(user_factory):
    user = user_factory()

    assert isinstance(user, User)
