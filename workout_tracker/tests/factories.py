import pytest

import factory
from django.db.models.signals import post_save, pre_delete
from users.models import User
from muscles.models import MuscleSubportion, Muscle, MuscleGrouping
from equipment.models import Equipment

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

    @factory.post_generation
    def equipment(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.equipment.add(EquipmentFactory())


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(pre_delete)
class MuscleGroupingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'back{x}')
    snames = factory.Sequence(lambda x: [f'Back{x}'])

    class Meta:
        model = 'muscles.MuscleGrouping'

    @factory.post_generation
    def muscles(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.muscles.add(MuscleFactory(subportions=1))


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(pre_delete)
class MuscleFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'traps{x}')
    snames = factory.Sequence(lambda x: [f'Traps{x}', f'trap{x}'])

    class Meta:
        model = 'muscles.Muscle'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        muscle = manager.create(*args, **kwargs)
        grouping = MuscleGroupingFactory()
        grouping.muscles.add(muscle)
        return muscle

    @factory.post_generation
    def subportions(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.subportions.add(MuscleSubportionFactory())


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(pre_delete)
class MuscleSubportionFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda x: f'upper traps{x}')
    snames = factory.Sequence(lambda x: [f'Upper traps{x}', f'uppertraps{x}'])

    class Meta:
        model = 'muscles.MuscleSubportion'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        subportion = manager.create(*args, **kwargs)
        muscle = MuscleFactory()
        muscle.subportions.add(subportion)
        return subportion


class EquipmentFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'barbell{x}')
    snames = factory.Sequence(lambda x: [f'Barbell{x}', f'bar bell{x}'])

    class Meta:
        model = 'equipment.Equipment'


@pytest.mark.django_db
def test_user_factory(user_factory):
    user = user_factory()

    assert isinstance(user, User)


@pytest.mark.django_db
def test_muscle_subportion_factory(muscle_subportion_factory):
    grouping = muscle_subportion_factory()

    assert isinstance(grouping, MuscleSubportion)
    assert MuscleSubportion.objects.all().count() == 1
    assert Muscle.objects.all().count() == 1
    assert MuscleGrouping.objects.all().count() == 1


@pytest.mark.parametrize('muscle_factory, num_subportions, expected_grouping, expected_muscle, expected_subportion', [
    (None, 0, 1, 1, 0),
    (None, 1, 2, 2, 1),
    (None, 2, 3, 3, 2)
], indirect=['muscle_factory'])
@pytest.mark.django_db
def test_muscle_factory(muscle_factory, num_subportions, expected_grouping, expected_muscle, expected_subportion):
    muscle = muscle_factory(subportions=num_subportions)

    assert isinstance(muscle, Muscle)
    assert muscle.subportions.all().count() == num_subportions
    assert Muscle.objects.all().count() == expected_muscle
    assert MuscleGrouping.objects.all().count() == expected_grouping
    assert MuscleSubportion.objects.all().count() == expected_subportion


@pytest.mark.parametrize('muscle_grouping_factory, num_muscles, expected_grouping, expected_muscle, expected_subportion', [
    (None, 0, 1, 0, 0),
    (None, 1, 3, 2, 1),
    (None, 2, 5, 4, 2)
], indirect=['muscle_grouping_factory'])
@pytest.mark.django_db
def test_muscle_grouping_factory(muscle_grouping_factory, num_muscles, expected_grouping, expected_muscle, expected_subportion):
    grouping = muscle_grouping_factory(muscles=num_muscles)

    assert isinstance(grouping, MuscleGrouping)
    assert grouping.muscles.all().count() == num_muscles
    assert MuscleGrouping.objects.all().count() == expected_grouping
    assert Muscle.objects.all().count() == expected_muscle
    assert MuscleSubportion.objects.all().count() == expected_subportion


@pytest.mark.django_db
def test_equipment_factory(equipment_factory):
    equipment = equipment_factory()

    assert isinstance(equipment, Equipment)
    assert isinstance(equipment.owner, User)


@pytest.mark.django_db
def test_user_factory_with_equipment(user_factory):
    num_equipment = 5
    user = user_factory(equipment=num_equipment)

    user_equipment = user.equipment.all()
    assert user_equipment.count() == num_equipment
    for equipment in user_equipment:
        assert equipment.owner == user
